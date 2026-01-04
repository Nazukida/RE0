# Multiply 3 by 2
print(3 * 2)

for i in range(3, 6):
    print(i)
    print(i * 2)
    
planet = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
my_planet = [p.upper() + "11" for p in planet if len(p) < 6]

print(my_planet)