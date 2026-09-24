"""faker.py
This module provides functions to generate fake data for testing purposes."""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-self

import random
from faker import Faker

fake = Faker()

def get_module_data(template: dict, context=None):
    """Generate data using template with shared context for related fields"""
    if context is None:
        context = {}
    result = {}
    
    for field_name, faker_func in template.items():
        # Pass context to the faker function
        if callable(faker_func):
            try:
                # Try calling with context first
                value = faker_func(context)
            except TypeError:
                # Fallback to calling without context for simple functions
                value = faker_func()
        else:
            value = faker_func
            
        result[field_name] = value
        # Store generated value in context for other fields to use
        context[field_name] = value
    
    return result

def create_module_template(moduleData: list,mode:str = "api"):
    template = {}
    for field in moduleData:
        template[field["name"]] = create_function(field,mode)
    return template


def create_function(field: dict,mode:str = "api"):
    field_name_lower = field["name"].lower()
    
    # Handle dynamic enum that depends on parent
    if field.get("type") == "dynamic_enum" and field.get("parent_field"):
        return create_dynamic_enum_function(field)
    
    # Handle regular enum
    if field.get("type") == "enum":
        return create_enum_function(field)
    
    # Priority overrides based on field name
    if "phone" in field_name_lower or "mobile" in field_name_lower:
        return lambda context=None: fake.numerify("##########")
    if "name" in field_name_lower:
        return lambda context=None: fake.name()
    if "url" in field_name_lower or "link" in field_name_lower:
        return lambda context=None: fake.url()

    # General field type-based logic
    match field["type"]:
        case "name":
            return lambda context=None: fake.name()
        case "bool":
            return lambda context=None: random.choice([True, False])
        case "currency":
            return lambda context=None: round(random.uniform(10, 10000), 2)
        # case "date":
        #     return lambda context=None: fake.date()
        # case "datetimecombo":
        #     return lambda context=None: fake.date_time().strftime("%Y-%m-%d %H:%M:%S")
        case "decimal":
            return lambda context=None: round(random.uniform(1.0, 1000.0), 4)
        case "float":
            return lambda context=None: round(random.uniform(1.0, 1000.0), 2)
        case "int":
            return lambda context=None: random.randint(1, 10000)
        case "phone":
            return lambda context=None: fake.numerify("##########")
        case "text":
            return lambda context=None: fake.paragraph(nb_sentences=3)
        case "url":
            return lambda context=None: fake.url()
        case "email":
            if mode == "csv":
                return lambda context=None: fake.safe_email()
            else:
                return lambda context=None: {
                    "email": fake.safe_email(),
                    "primary": True,
                    "optOut": False,
                    "invalid": False,
                    "deleted": False,
                    "error": False
                }
        case "varchar":
            return lambda context=None: fake.word()
        case _:
            return lambda context=None: None

def create_enum_function(field: dict):
    """Create function for regular enum field"""
    if (field.get("options") is None) or (not field.get("options")):
        return lambda context=None: ""
    enum_values = list(field.get("options", {}).values())
    return lambda context=None: random.choice(enum_values)

def create_dynamic_enum_function(field: dict):
    """Create function for dynamic enum that depends on parent field"""
    parent_field = field.get("parentenum")
    # This should contain mapping like: {"parent_value1": ["child1", "child2"], "parent_value2": ["child3", "child4"]}
    options = list(field.get("options", {}).values())
    default_values = field.get("default_values", [""])
    
    def dynamic_enum_generator(context):
        if context and parent_field in context:
            parent_value = context[parent_field]
            available_options = [opt for opt in options if parent_value in opt]
            print(available_options)
            return random.choice(available_options)
        else:
            # If parent not generated yet or not in context, use default
            return random.choice(default_values)
    
    return dynamic_enum_generator
