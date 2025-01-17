import streamlit as st
import os
import tempfile
import shutil
from folder_scraper import process_folder, process_zip_file
from pathlib import Path

st.title("Folder Content Processor")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Folder Path", "File Upload"])

with tab1:
    st.header("Process Folder")
    folder_path = st.text_input("Enter folder path (e.g., /path/to/your/folder)")
    
    # Exclusion patterns for folder processing
    exclude_patterns_folder = st.text_input(
        "Folders to exclude (space-separated)", 
        value="venv __pycache__ .git",
        key="exclude_folder"
    ).split()
    
    if st.button("Process Folder", key="process_folder"):
        if folder_path and os.path.exists(folder_path):
            with st.spinner("Processing folder..."):
                try:
                    process_folder(folder_path)
                    st.success(f"Folder processed successfully!")
                    
                    # Find and offer download of the generated file
                    folder_name = os.path.basename(folder_path)
                    output_file = f"combined_{folder_name}.md"
                    if os.path.exists(output_file):
                        with open(output_file, "r", encoding="utf-8") as f:
                            st.download_button(
                                label="Download Results",
                                data=f.read(),
                                file_name=output_file,
                                mime="text/markdown"
                            )
                except Exception as e:
                    st.error(f"Error processing folder: {str(e)}")
        else:
            st.error("Please enter a valid folder path")

with tab2:
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Choose files to process", 
        accept_multiple_files=True,
        type=['zip', 'pdf', 'docx', 'txt', 'pptx', 'py', 'java', 'js', 'cpp', 'sql', 'json', 'yaml', 'yml', 'xml', 'html', 'css', 'md']
    )
    
    # Exclusion patterns for file processing
    exclude_patterns_files = st.text_input(
        "Folders to exclude (space-separated)", 
        value="venv __pycache__ .git",
        key="exclude_files"
    ).split()
    
    output_name = st.text_input("Output file name (without .md)", value="combined_upload")
    
    if st.button("Process Files", key="process_files") and uploaded_files:
        with st.spinner("Processing files..."):
            try:
                # Create a temporary directory to store uploaded files
                with tempfile.TemporaryDirectory() as temp_dir:
                    has_zip = False
                    # Save uploaded files to temp directory
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Check if this is a zip file
                        if uploaded_file.name.lower().endswith('.zip'):
                            has_zip = True
                            output_md = process_zip_file(file_path)
                    
                    # If no zip files were processed, process as regular folder
                    if not has_zip:
                        output_md = process_folder(temp_dir)
                    
                    # Rename the output file
                    if os.path.exists(output_md):
                        final_output = f"{output_name}.md"
                        shutil.move(output_md, final_output)
                        
                        # Offer download of the combined file
                        with open(final_output, "r", encoding="utf-8") as f:
                            st.download_button(
                                label="Download Combined Results",
                                data=f.read(),
                                file_name=final_output,
                                mime="text/markdown"
                            )
                        
                        st.success("Files processed successfully!")
            except Exception as e:
                st.error(f"Error processing files: {str(e)}")

# Add instructions
st.markdown("""
### Instructions:
#### Using Folder Path:
1. Enter the full path to the folder you want to process
2. Optionally specify folders to exclude
3. Click 'Process Folder'
4. Download the resulting markdown file

#### Using File Upload:
1. Upload multiple files or ZIP archives using the file uploader
2. Optionally specify folders to exclude
3. Provide a name for the output file
4. Click 'Process Files'
5. Download the combined markdown file

Supported file types: ZIP, PDF, DOCX, TXT, PPTX, and various code files (Python, Java, JavaScript, etc.)
""")

# Add a footer with version info
st.markdown("---")
st.markdown("v1.0 - Folder Content Processor") 