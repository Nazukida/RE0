import yaml
import torch
import argparse
import os
from src.models.net import get_model
from src.data.loader import get_loaders
from src.training.trainer import Trainer
from src.deploy.export import export_to_onnx, export_to_torchscript_mobile
from src.deploy.inference import Predictor
from src.utils.logger import setup_logger

def main(args):
    # Load configuration
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    logger = setup_logger(config['log_dir'])
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # ---------------------------------------------------------
    # Training Mode
    # ---------------------------------------------------------
    if args.mode == 'train':
        logger.info("Starting Mobile Lightweight Pet Recognition System Project...")
        logger.info(f"Using device: {device}")
        
        # Data Loading
        logger.info("Initializing Data Loaders...")
        train_loader, val_loader = get_loaders(config)
        
        # Model Initialization
        logger.info(f"Building Model: {config['model_name']}...")
        model = get_model(config)
        
        logger.info("Starting Training Workflows...")
        trainer = Trainer(model, train_loader, val_loader, config, device)
        trainer.run()
        logger.info("Training Complete.")
        
        # Auto export after training
        if args.export:
            logger.info("Exporting model for mobile deployment...")
            # Load best model
            best_model_path = f"{config['save_dir']}/best_model.pt"
            model.load_state_dict(torch.load(best_model_path))
            export_to_onnx(model.cpu(), config, output_path=f"{config['save_dir']}/mobile_pet_net.onnx")
            export_to_torchscript_mobile(model.cpu(), output_path=f"{config['save_dir']}/mobile_pet_net.ptl")

    # ---------------------------------------------------------
    # Inference Mode (Prediction)
    # ---------------------------------------------------------
    elif args.mode == 'predict':
        if not args.image:
            logger.error("Please provide an image path using --image argument.")
            return

        model_path = args.checkpoint if args.checkpoint else os.path.join(config['save_dir'], 'best_model.pt')
        logger.info(f"Loading model from {model_path}...")
        
        predictor = Predictor(config, model_path, device)
        result = predictor.predict(args.image)
        
        if "error" in result:
            logger.error(result["error"])
        else:
            print("\n" + "="*30)
            print(f"Image: {args.image}")
            print(f"Prediction: {result['class']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print("="*30 + "\n")

    # ---------------------------------------------------------
    # Export Mode
    # ---------------------------------------------------------
    elif args.mode == 'export':
        logger.info("Exporting Model...")
        checkpoint_path = args.checkpoint if args.checkpoint else os.path.join(config['save_dir'], 'best_model.pt')
        if not os.path.exists(checkpoint_path):
             logger.error(f"Checkpoint not found at {checkpoint_path}")
             return

        model = get_model(config)
        model.load_state_dict(torch.load(checkpoint_path, map_location='cpu'))
        export_to_onnx(model, config, output_path=f"{config['save_dir']}/exported_model.onnx")
        export_to_torchscript_mobile(model, output_path=f"{config['save_dir']}/exported_model.ptl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pet Recognition System")
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to config file')
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'predict', 'export'], help='Mode: train, predict or export')
    parser.add_argument('--block', type=str, help='(Optional) Specific block to visualize (not implemented yet)')
    parser.add_argument('--image', type=str, help='Path to image for prediction')
    parser.add_argument('--export', action='store_true', help='Export after training')
    parser.add_argument('--checkpoint', type=str, help='Checkpoint path')
    
    args = parser.parse_args()
    main(args)
