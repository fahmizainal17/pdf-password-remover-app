import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
import zipfile
from typing import List, Tuple
from component import page_style

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

    page_style()

    # Initialize session state for persistence
    if 'unlocked_files' not in st.session_state:
        st.session_state.unlocked_files = []
    if 'results' not in st.session_state:
        st.session_state.results = []

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
                        file.seek(0)
                        unlocked_bytes, success, message = unlock_pdf(file, passwords[file.name])
                        if success:
                            name_without_ext = os.path.splitext(file.name)[0]
                            output_filename = f"unlocked_{name_without_ext}.pdf"
                            unlocked_files.append((output_filename, unlocked_bytes))
                            results.append((file.name, "✅ Success", "Password removed successfully"))
                        else:
                            results.append((file.name, "❌ Failed", message))
                    else:
                        results.append((file.name, "⚠️ Skipped", "No password provided"))
                    progress_bar.progress((i + 1) / len(uploaded_files))

                status_text.text("Processing complete!")
                # Save to session state
                st.session_state.unlocked_files = unlocked_files
                st.session_state.results = results

            # Display results and download options if available
            if st.session_state.results:
                st.header("📊 Results")
                for fname, status, msg in st.session_state.results:
                    if "Success" in status:
                        st.success(f"**{fname}**: {msg}")
                    elif "Failed" in status:
                        st.error(f"**{fname}**: {msg}")
                    else:
                        st.warning(f"**{fname}**: {msg}")

                if st.session_state.unlocked_files:
                    st.header("⬇️ Download Unlocked PDFs")
                    if len(st.session_state.unlocked_files) == 1:
                        fname, pdf_bytes = st.session_state.unlocked_files[0]
                        st.download_button(
                            label=f"Download {fname}",
                            data=pdf_bytes,
                            file_name=fname,
                            mime="application/pdf"
                        )
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            zip_bytes = create_zip_file(st.session_state.unlocked_files)
                            st.download_button(
                                label="Download All as ZIP",
                                data=zip_bytes,
                                file_name="unlocked_pdfs.zip",
                                mime="application/zip"
                            )
                        with col2:
                            st.subheader("Individual Downloads:")
                            for fname, pdf_bytes in st.session_state.unlocked_files:
                                st.download_button(
                                    label=f"📄 {fname}",
                                    data=pdf_bytes,
                                    file_name=fname,
                                    mime="application/pdf",
                                    key=f"download_{fname}"
                                )

# Run the main function
main()
