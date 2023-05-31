import os
# Set the DJANGO_SETTINGS_MODULE environment variable
# so that Django knows which settings to use, in this case, my_project.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")
import django
django.setup()
from django.apps import apps
from django.db import models

# Mapping of common Django field types to dbdiagram.io field types
FIELD_TYPE_MAP = {
    models.AutoField: "int [pk, increment]",
    models.CharField: "varchar",
    models.TextField: "text",
    models.IntegerField: "int",
    models.PositiveIntegerField: "int",
    models.PositiveSmallIntegerField: "int",
    models.BooleanField: "boolean",
    models.DateField: "date",
    models.DateTimeField: "datetime",
    models.ForeignKey: "int",  # Will be handled specially
    models.FileField: "FileField",
    models.DecimalField: "decimal",
    models.FloatField: "float",
    models.ImageField: "image",
    models.EmailField: "email",
    # Add more field types as needed
}

def generate_field_line(field):
    field_type = FIELD_TYPE_MAP.get(type(field))
    if field_type is None:
        print(f"Warning: Unknown field type: {field, type(field)}")
        return None
    if isinstance(field, models.ForeignKey):
        ref_table_name = field.related_model._meta.db_table
        return f"  {field.name} {field_type} [ref: > {ref_table_name}.id]"
    return f"  {field.name} {field_type}"

def process_m2m_table(m2m_tables, field, table_name):
    # Since it is a better practice to explicitly define a through table for a ManyToManyField,
    # the default behavior in this code is to not generate a through table for a ManyToManyField.
    # However you can uncomment the following lines, if you would like do so for your project.
    ### START BELOW THIS LINE ###
    # m2m_table_name = f"{table_name}_{field.name}"
    # ref_table_name = field.related_model._meta.db_table
    # m2m_tables += f"Table {m2m_table_name} {{\n"
    # m2m_tables += f"  {table_name}_id int [ref: > {table_name}.id]\n"
    # m2m_tables += f"  {field.name}_id int [ref: > {ref_table_name}.id]\n"
    # m2m_tables += "}\n"
    ### END ABOVE THIS LINE ###
    return m2m_tables

def generate_dbdiagram_code(model):
    m2m_tables = ""
    table_name = model._meta.db_table
    fields = model._meta.get_fields()
    lines = [f"\nTable {table_name} {{"]
    for field in fields:
        if isinstance(field, models.ManyToManyField):
            m2m_tables = process_m2m_table(m2m_tables, field, table_name)
        else:
            line = generate_field_line(field)
            if line is not None:
                lines.append(line)
    lines.append("}")
    return "\n".join(lines) + m2m_tables

if __name__ == "__main__":
    # Write the generated code to a file
    with open("dbdiagram.txt", "w") as f:
        for model in apps.get_models():
            f.write(generate_dbdiagram_code(model))
