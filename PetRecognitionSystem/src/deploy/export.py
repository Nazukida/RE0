import torch
import onnx
import os

def export_to_onnx(model, config, output_path="mobile_model.onnx"):
    """
    Exports the trained PyTorch model to ONNX format for mobile deployment.
    """
    model.eval()
    dummy_input = torch.randn(1, 3, config['image_size'], config['image_size'])
    
    # Export the model
    torch.onnx.export(
        model,               # model being run
        dummy_input,         # model input (or a tuple for multiple inputs)
        output_path,         # where to save the model (can be a file or file-like object)
        export_params=True,  # store the trained parameter weights inside the model file
        opset_version=11,    # the ONNX version to export the model to
        do_constant_folding=True,  # whether to execute constant folding for optimization
        input_names = ['input'],   # the model's input names
        output_names = ['output'], # the model's output names
        dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
                      'output' : {0 : 'batch_size'}}
    )
    print(f"Model exported to {output_path}")
    
    # Verify the ONNX model
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    print("ONNX model verified successfully!")
    
def export_to_torchscript_mobile(model, output_path="mobile_model.ptl"):
    """
    Exports the model to TorchScript specifically optimized for mobile.
    """
    model.eval()
    example_input = torch.rand(1, 3, 224, 224)
    traced_script_module = torch.jit.trace(model, example_input)
    traced_script_module_optimized = torch.utils.mobile_optimizer.optimize_for_mobile(traced_script_module)
    traced_script_module_optimized._save_for_lite_interpreter(output_path)
    print(f"TorchScript Mobile model saved to {output_path}")
