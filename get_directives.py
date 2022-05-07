"""
Script to generate the list of roles and directives for the Toolbox class.

Requires ``sphobjinv`` (``pip install sphobjinv``).
"""

# 3rd party
import sphobjinv

inventory = sphobjinv.inventory.Inventory(url="https://sphinx-toolbox.readthedocs.io/en/latest/objects.inv")

directives = []
roles = []

obj: sphobjinv.data.DataObjStr
for obj in inventory.objects:
	if obj.domain == "rst":
		if obj.role == "directive":
			# print(obj)
			directives.append(obj.name)
		elif obj.role == "role":
			roles.append(obj.name)
"""
		self.roles.update([
				"asset",
				"bold-title",

				"wikipedia",
				])

		self.directives.update([
				"actions-shield",

				])
"""

print("\t\tself.roles.update([")
for role in roles:
	print(f'				"{role}",')
print("\t\t\t\t])")
print('')
print("\t\tself.directives.update([")
for directive in directives:
	print(f'				"{directive}",')
print("\t\t\t\t])")
