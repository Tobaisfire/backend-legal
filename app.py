from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import fitz  # PyMuPDF
import io
import os
from source.summarizer import legal_sys, calculate_optimal_summary

app = FastAPI()

# Get allowed origins from environment or use defaults


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://legal-ai-pack.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/summarize")
async def summarize_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    try:
        print("---------------HIT THE API---------------")
        legal_system = legal_sys()
        print("---------------Created the object---------------")
        
        content = ""
        summary_totals = None
        total_words = 1000  # Default value for text-only input
        
        if file:
            # Check if it's a PDF
            if file.filename.lower().endswith('.pdf'):
                # Read PDF content
                print("---------------PDF FILE---------------")
                pdf_bytes = await file.read()
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

                
                summary_totals = calculate_optimal_summary(pdf_document.page_count)
                total_words = summary_totals["total_words"]
                
                
                # Extract text from all pages
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    content += f"\n--- Page {page_num + 1} ---\n\n"
                    content += page.get_text()
                
                pdf_document.close()
            else:
                print("---------------OTHER FILE---------------")
                # Handle other file types (TXT, etc.)
                file_content = await file
                if file_content.filename.lower().endswith('.pdf'):
                # Read PDF content
                    pdf_bytes = await file_content.read()
                    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                    summary_totals = calculate_optimal_summary(pdf_document.page_count)
                    total_words = summary_totals["total_words"]                
                else:
                    content = file_content.read()
                    # Estimate pages for text-only input
                    estimated_pages = len(content.split()) / 300
                    summary_totals = calculate_optimal_summary(estimated_pages)    
        
        if text:
            if content: 
                content += "\n\n" + text
            else:
                content = text
                # Estimate pages for text-only input
                estimated_pages = len(content.split()) / 300
                summary_totals = calculate_optimal_summary(estimated_pages)
                total_words = summary_totals["total_words"]
        
        if not content.strip():
            raise HTTPException(status_code=400, detail="No content found in the document")
        
        print(summary_totals)
        summary = legal_system.summarize_document(content, total_words)
        
        return {
            "content": summary,
            "status": "success",
            "summary_totals": summary_totals
        }
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error occurred: {str(e)}")
        print(f"Traceback: {error_traceback}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Legal Document Summarizer API"}