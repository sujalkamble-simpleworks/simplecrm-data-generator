# from createrecord import CreateRecord
import streamlit as st
import time
import uuid
import os

from recordCreator import RecordCreator

st.set_page_config(page_title="Data Generator", layout="wide")

with st.sidebar:
    st.write("# Data Generator")
    st.write("App to create Data for SimpleCRM instances.")

# Initialize session state for modules
if "modules" not in st.session_state:
    st.session_state.modules = {}

if "generating" not in st.session_state:
    st.session_state.generating = False

if "url" not in st.session_state:
    st.session_state.url = "https://internalcrmv267baseline.simplecrmondemand.com/Api/V8"

if "users" not in st.session_state:
    st.session_state.users = []

if "username" not in st.session_state:
    st.session_state.username = os.getenv("SIMPLECRM_USERNAME", "admin")

if "password" not in st.session_state:
    st.session_state.password = os.getenv("SIMPLECRM_PASSWORD", "")

with st.sidebar:
    if st.session_state.generating is False:
        st.session_state.url = st.text_input(
            "Enter the API URL of your SimpleCRM instance", st.session_state.url
        )
        st.session_state.username = st.text_input(
            "Username", st.session_state.username
        )
        st.session_state.password = st.text_input(
            "RSA-encrypted API password",
            st.session_state.password,
            type="password",
        )
    else:
        st.write(f"SimpleCRM Instance URL: {st.session_state.url}")


# Function to add a new module
def add_module():
    module_id = str(uuid.uuid4())
    st.session_state.modules[module_id] = {
        "name": f"Module {len(st.session_state.modules) + 1}",
        "backend_name": f"module_{len(st.session_state.modules) + 1}",
        "records": 10,
    }


# Function to remove a module
def remove_module(module_id):
    if module_id in st.session_state.modules:
        del st.session_state.modules[module_id]


if not st.session_state.generating:
    # UI Controls
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Add Module", type="primary"):
            add_module()

    with col2:
        if st.button("Clear All Modules", type="secondary"):
            st.session_state.modules = {}

    st.divider()

    # Display modules
    if st.session_state.modules:
        st.subheader(f"Modules ({len(st.session_state.modules)})")

        for module_id, module_data in st.session_state.modules.items():
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    # Module configuration inputs
                    module_name = st.text_input(
                        "Module Name",
                        value=module_data["name"],
                        key=f"name_{module_id}",
                    )

                    backend_name = st.text_input(
                        "Backend Name",
                        value=module_data["backend_name"],
                        key=f"backend_{module_id}",
                    )

                    num_records = st.number_input(
                        "Number of Records",
                        min_value=1,
                        value=module_data["records"],
                        key=f"records_{module_id}",
                    )

                    # Update the session state with current values
                    st.session_state.modules[module_id] = {
                        "name": module_name,
                        "backend_name": backend_name,
                        "records": num_records,
                    }

                with col2:
                    st.write("")  # Add some spacing
                    st.write("")  # Add some spacing
                    if st.button(
                        "🗑️ Remove", key=f"remove_{module_id}", type="secondary"
                    ):
                        remove_module(module_id)
                        st.rerun()

        # Display current modules data
        st.divider()
        st.subheader("Current Modules Data")
        st.json(st.session_state.modules)

    else:
        st.info("No modules added yet. Click 'Add Module' to get started!")
else:
    st.empty()

with st.sidebar:
    if st.button(
        "Generate Data",
        type="primary",
        disabled=st.session_state.generating or not st.session_state.modules,
    ):
        st.session_state.generating = True
        st.rerun()

if st.session_state.generating:
    st.header("Data Generation Progress")
    try:
        generator = RecordCreator(
            {"username": st.session_state.username, "password": st.session_state.password},
            st.session_state.url,
        )
    except Exception as error:
        st.session_state.generating = False
        st.error(f"Authentication failed: {error}")
        st.stop()
    total_records = sum(module["records"] for module in st.session_state.modules.values())
    
    with st.spinner("Processign modules..."):
        generator.process_modules(st.session_state.modules,mode="csv")
    
    # Create progress bar and empty container for results
    progress_bar = st.progress(0)
    results_container = st.empty()
    # Process results with progress updates
    
    start_time = time.time()
    
    generated_files = generator.generate_csv(
        st.session_state.modules,
        progress_callback=lambda completed: progress_bar.progress(
            completed / total_records
        ),
    )
    
    # results = {}
    # for module in st.session_state.modules.values():
    #     results[module["name"]] = {"success": 0, "failed": 0}
    
    # for i, result in enumerate(generator.create_records(st.session_state.modules)):
    #     if result["status"] == "success":
    #         results[result["module"]]["success"] += 1
    #     else:
    #     progress = (i + 1) / total_records
    #     progress_bar.progress(progress)
        
    #     # Show progress message during processing
    #     results_container.info(f"Data generation in progress... {i + 1}/{total_records} records")
        
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Final results
    results_container.success(f"Completed! Processed {total_records} records.")
    st.write(f"Time taken: {elapsed_time:.2f} seconds")
    st.subheader("Download CSV files")
    for filename in generated_files:
        with open(filename, "rb") as file:
            st.download_button(
                label=f"Download {os.path.basename(filename)}",
                data=file.read(),
                file_name=os.path.basename(filename),
                mime="text/csv",
            )
    # st.json(results)
    
    # Reset generating state to allow new operations
    st.session_state.generating = False

    if st.button("Generate More", type="primary") :
        st.rerun()
