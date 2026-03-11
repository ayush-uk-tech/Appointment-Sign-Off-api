from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
import fitz
import os

app = FastAPI()

# Naye template ke hisaab se Data Model
class EmployeeSignOffData(BaseModel):
    # Top Section
    client_name_top: str        # CLIENT NAME [cite: 6]
    name_top: str               # NAME [cite: 7]
    email_address: str          # E-MAIL ADDRESS [cite: 8]
    
    # Table Section [cite: 11]
    candidate_name: str         # NAME OF CANDIDATE/EMPLOYEE
    position: str               # POSITION
    start_date: str             # START DATE
    annual_salary: str          # ANNUAL SALARY COST
    annual_tech_cost: str       # ANNUAL TECHNOLOGY COST
    annual_office_cost: str     # ANNUAL OFFICE COST
    total_cost: str             # TOTAL COST TO BE INVOICED MONTHLY
    
    # Other Details Section [cite: 11]
    annual_leave: str           # Annual Leave
    probation_period: str       # Probation Period
    notice_period: str          # Notice period
    
    # Bottom Signature Section
    client_bottom: str          # CLIENT [cite: 14]
    signed: str                 # SIGNED [cite: 15]
    name_bottom: str            # NAME [cite: 16]
    position_bottom: str        # POSITION [cite: 17]
    date_bottom: str            # DATE [cite: 18]

@app.post("/generate-employee-signoff")
async def generate_signoff_pdf(data: EmployeeSignOffData):
    try:
        # Tumhare naye template ka naam (ensure karna ye file api/ folder me ho)
        template_path = os.path.join(os.path.dirname(__file__), "template.pdf")
        
        doc = fitz.open(template_path)
        page = doc[0]
        
        # ⚠️ PRO TIP: Bhai, in 'x' aur 'y' coordinates ko apne template ke exact layout 
        # ke hisaab se adjust kar lena. Maine abhi dummy coordinates dale hain.
        insertions = [
            {"text": data.client_name_top, "x": 150, "y": 100},
            {"text": data.name_top, "x": 150, "y": 120},
            {"text": data.email_address, "x": 150, "y": 140},
            
            {"text": data.candidate_name, "x": 250, "y": 200},
            {"text": data.position, "x": 250, "y": 220},
            {"text": data.start_date, "x": 250, "y": 240},
            {"text": data.annual_salary, "x": 250, "y": 260},
            {"text": data.annual_tech_cost, "x": 250, "y": 280},
            {"text": data.annual_office_cost, "x": 250, "y": 300},
            {"text": data.total_cost, "x": 250, "y": 320},
            
            {"text": data.annual_leave, "x": 250, "y": 360},
            {"text": data.probation_period, "x": 250, "y": 380},
            {"text": data.notice_period, "x": 250, "y": 400},
            
            {"text": data.client_bottom, "x": 100, "y": 550},
            {"text": data.signed, "x": 100, "y": 570},
            {"text": data.name_bottom, "x": 100, "y": 590},
            {"text": data.position_bottom, "x": 100, "y": 610},
            {"text": data.date_bottom, "x": 100, "y": 630},
        ]
        
        # Loop karke PDF par text likhna
        for item in insertions:
            page.insert_text(
                fitz.Point(item['x'], item['y']),
                str(item['text']),
                fontsize=9,
                fontname="helv",
                color=(0, 0, 0)
            )
            
        pdf_bytes = doc.write()
        doc.close()
        
        # Dynamic filename banana: candidate_name + client_name
        # Spaces ko underscore me convert kar rahe hain taaki URL/file-system friendly rahe
        safe_candidate_name = data.candidate_name.replace(" ", "_")
        safe_client_name = data.client_name_top.replace(" ", "_")
        custom_filename = f"{safe_candidate_name}_{safe_client_name}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={custom_filename}"
            }
        )
    except Exception as e:
        return {"error": f"Error aagaya: {str(e)}"}
