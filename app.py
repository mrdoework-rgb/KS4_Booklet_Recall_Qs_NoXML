import streamlit as st
import json
from io import BytesIO
from docxtpl import DocxTemplate

def process_template(template_file, json_data):
    """
    Takes the uploaded Word document and the JSON data, and uses
    docxtpl to render the Jinja tags natively.
    """
    # Initialize the template
    doc = DocxTemplate(template_file)
    
    # Render the template with the JSON data (which acts as our context dictionary)
    doc.render(json_data)
    
    # Save to a BytesIO object for downloading
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    
    return output

# --- Streamlit UI ---
st.set_page_config(page_title="Revision Template Generator", layout="centered")

st.title("📄 Revision Template Generator (XML-Free)")
st.markdown("Upload your `.docx` template (configured with docxtpl tags) and paste your JSON data.")

uploaded_template = st.file_uploader("1. Upload your Template Recall.docx", type=["docx"])
json_input = st.text_area("2. Paste your JSON Data", height=300, placeholder='{"revision_sections": [...]}')

if st.button("Generate Document", type="primary"):
    if not uploaded_template:
        st.warning("Please upload a Word document template.")
    elif not json_input.strip():
        st.warning("Please paste your JSON data.")
    else:
        try:
            # Parse JSON
            parsed_json = json.loads(json_input)
            
            with st.spinner("Generating document..."):
                # Process the document
                output_docx = process_template(uploaded_template, parsed_json)
                
                st.success("Document generated successfully!")
                
                # Download Button
                st.download_button(
                    label="⬇️ Download Populated Word Document",
                    data=output_docx,
                    file_name="Populated_Revision_Document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your JSON data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
