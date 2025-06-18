import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
import zipfile
from typing import List, Tuple

def unlock_pdf(pdf_file, password: str) -> Tuple[bytes, bool, str]:
    """
    Unlock a PDF file with the given password
    Returns: (unlocked_pdf_bytes, success, error_message)
    """
    try:
        # Read the PDF
        reader = PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if not reader.is_encrypted:
            return None, False, "PDF is not password protected"
        
        # Try to decrypt with the provided password
        if not reader.decrypt(password):
            return None, False, "Incorrect password"
        
        # Create a new PDF writer
        writer = PdfWriter()
        
        # Copy all pages to the writer
        for page in reader.pages:
            writer.add_page(page)
        
        # Write to bytes buffer
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer.getvalue(), True, "Success"
        
    except Exception as e:
        return None, False, f"Error processing PDF: {str(e)}"

def create_zip_file(unlocked_files: List[Tuple[str, bytes]]) -> bytes:
    """
    Create a ZIP file containing multiple unlocked PDFs
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, pdf_bytes in unlocked_files:
            zip_file.writestr(filename, pdf_bytes)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    st.set_page_config(
        page_title="PDF Password Remover",
        page_icon="🔓",
        layout="wide"
    )
    
    st.title("🔓 PDF Password Remover")
    st.markdown("Upload password-protected PDFs and remove their passwords for easier access.")
    
    # File upload section
    st.header("📁 Upload PDF Files")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="You can upload multiple PDF files at once"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Password input section
        st.header("🔑 Password Settings")
        
        # Toggle for same password
        use_same_password = st.toggle(
            "Use the same password for all PDFs",
            value=True,
            help="Enable this if all your PDFs have the same password"
        )
        
        passwords = {}
        
        if use_same_password:
            # Single password input
            common_password = st.text_input(
                "Enter password for all PDFs:",
                type="password",
                help="This password will be used for all uploaded PDFs"
            )
            
            if common_password:
                for file in uploaded_files:
                    passwords[file.name] = common_password
        else:
            # Individual password inputs
            st.subheader("Enter password for each PDF:")
            for file in uploaded_files:
                password = st.text_input(
                    f"Password for {file.name}:",
                    type="password",
                    key=f"pwd_{file.name}"
                )
                if password:
                    passwords[file.name] = password
        
        # Process PDFs section
        if passwords:
            st.header("🔄 Process PDFs")
            
            if st.button("Remove Passwords", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                unlocked_files = []
                results = []
                
                for i, file in enumerate(uploaded_files):
                    if file.name in passwords:
                        status_text.text(f"Processing {file.name}...")
                        
                        # Reset file pointer
                        file.seek(0)
                        
                        # Try to unlock the PDF
                        unlocked_bytes, success, message = unlock_pdf(file, passwords[file.name])
                        
                        if success:
                            # Generate output filename
                            name_without_ext = os.path.splitext(file.name)[0]
                            output_filename = f"unlocked_{name_without_ext}.pdf"
                            unlocked_files.append((output_filename, unlocked_bytes))
                            results.append((file.name, "✅ Success", "Password removed successfully"))
                        else:
                            results.append((file.name, "❌ Failed", message))
                    else:
                        results.append((file.name, "⚠️ Skipped", "No password provided"))
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.text("Processing complete!")
                
                # Display results
                st.header("📊 Results")
                
                for filename, status, message in results:
                    if "Success" in status:
                        st.success(f"**{filename}**: {message}")
                    elif "Failed" in status:
                        st.error(f"**{filename}**: {message}")
                    else:
                        st.warning(f"**{filename}**: {message}")
                
                # Download section
                if unlocked_files:
                    st.header("⬇️ Download Unlocked PDFs")
                    
                    if len(unlocked_files) == 1:
                        # Single file download
                        filename, pdf_bytes = unlocked_files[0]
                        st.download_button(
                            label=f"Download {filename}",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf"
                        )
                    else:
                        # Multiple files - create ZIP
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Download as ZIP
                            zip_bytes = create_zip_file(unlocked_files)
                            st.download_button(
                                label="Download All as ZIP",
                                data=zip_bytes,
                                file_name="unlocked_pdfs.zip",
                                mime="application/zip"
                            )
                        
                        with col2:
                            # Individual downloads
                            st.subheader("Individual Downloads:")
                            for filename, pdf_bytes in unlocked_files:
                                st.download_button(
                                    label=f"📄 {filename}",
                                    data=pdf_bytes,
                                    file_name=filename,
                                    mime="application/pdf",
                                    key=f"download_{filename}"
                                )
    
    # Instructions section
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        1. **Upload PDFs**: Click on the file uploader and select one or more password-protected PDF files
        2. **Set Passwords**: 
           - Toggle ON "Use same password" if all PDFs have the same password
           - Toggle OFF to enter individual passwords for each PDF
        3. **Process**: Click "Remove Passwords" to unlock your PDFs
        4. **Download**: Download individual files or all files as a ZIP archive
        
        **Note**: This app removes passwords from PDFs for convenience. Make sure you have the right to modify these documents.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# Run the main function
main()