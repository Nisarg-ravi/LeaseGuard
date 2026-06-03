"""
PDF report generation service.
"""
import logging
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from typing import List, Dict, Any
from io import BytesIO

from app.models import Contract, ContractAnalysis, Clause

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates PDF reports for contract analysis."""
    
    @staticmethod
    def generate_report(
        contract: Contract,
        analysis: ContractAnalysis,
        clauses: List[Clause]
    ) -> BytesIO:
        """
        Generate a PDF report for contract analysis.
        
        Args:
            contract: Contract model
            analysis: Analysis results
            clauses: List of clause models
            
        Returns:
            BytesIO object with PDF data
        """
        pdf_buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="LeaseGuard Contract Analysis Report"
        )
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leading=12
        )
        
        # Build story
        story = []
        
        # Header
        story.append(Paragraph("LeaseGuard", title_style))
        story.append(Paragraph("Contract Analysis Report", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Report info
        info_data = [
            ["Document:", contract.original_filename],
            ["Analysis Date:", datetime.now().strftime("%B %d, %Y")],
            ["Total Pages:", str(contract.total_pages)],
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Risk Summary
        story.append(Paragraph("Risk Assessment Summary", heading_style))
        
        risk_color = ReportGenerator._get_risk_color(analysis.overall_risk_score)
        
        summary_data = [
            ["Overall Risk Score:", f"{analysis.overall_risk_score:.1f}/100", ""],
            ["Risk Category:", ReportGenerator._get_risk_category(analysis.overall_risk_score), ""],
            ["Total Clauses Analyzed:", str(analysis.total_clauses), ""],
            ["High Risk Clauses:", str(analysis.high_risk_count), ""],
            ["Medium Risk Clauses:", str(analysis.medium_risk_count), ""],
            ["Low Risk Clauses:", str(analysis.low_risk_count), ""],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Summary", heading_style))
        story.append(Paragraph(analysis.summary, normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Detailed Analysis
        story.append(Paragraph("Detailed Clause Analysis", heading_style))
        
        for clause in clauses:
            risk_level_text = clause.risk_level.value.upper()
            risk_color = ReportGenerator._get_risk_color_for_level(clause.risk_level.value)
            
            story.append(Paragraph(
                f"<b>Clause {clause.clause_number}: {risk_level_text}</b> "
                f"(Score: {clause.risk_score:.1f}/100)",
                ParagraphStyle(
                    'ClauseTitle',
                    parent=normal_style,
                    textColor=risk_color,
                    fontName='Helvetica-Bold'
                )
            ))
            
            # Original text
            story.append(Paragraph(
                f"<b>Original Text:</b><br/><i>{clause.original_text[:200]}...</i>",
                normal_style
            ))
            
            # Parse explanation if available
            if clause.explanation:
                try:
                    explanation = json.loads(clause.explanation)
                    story.append(Paragraph(
                        f"<b>Plain English:</b><br/>{explanation.get('plain_english_summary', '')}",
                        normal_style
                    ))
                except:
                    pass
            
            # Risks
            if clause.rule_based_risks:
                try:
                    risks = json.loads(clause.rule_based_risks)
                    if risks:
                        story.append(Paragraph("<b>Identified Risks:</b>", normal_style))
                        for risk in risks[:3]:  # Top 3 risks
                            story.append(Paragraph(
                                f"• {risk.get('rule', 'Unknown')}: {risk.get('reason', '')}",
                                ParagraphStyle('Risk', parent=normal_style, leftIndent=0.2*inch)
                            ))
                except:
                    pass
            
            story.append(Spacer(1, 0.15*inch))
        
        # Recommendations
        story.append(PageBreak())
        story.append(Paragraph("Recommendations", heading_style))
        
        recommendations = [
            "Review all flagged high-risk clauses carefully before signing",
            "Discuss concerning clauses with the landlord or property manager",
            "Consider consulting with a tenant rights organization or lawyer",
            "Research similar lease agreements in your area for comparison",
            "Never sign under pressure; take time to fully understand the agreement",
            "Keep a copy of the final signed lease for your records",
        ]
        
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", normal_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(Paragraph(
            "<i>LeaseGuard helps tenants understand rental agreements. "
            "This report is for informational purposes only and does not constitute legal advice. "
            "For legal advice, consult with a qualified attorney.</i>",
            ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey)
        ))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        
        logger.info("Report generated successfully")
        return pdf_buffer
    
    @staticmethod
    def _get_risk_color(score: float) -> colors.Color:
        """Get color based on risk score."""
        if score >= 80:
            return colors.HexColor('#DC2626')  # Red
        elif score >= 51:
            return colors.HexColor('#F59E0B')  # Amber
        elif score >= 21:
            return colors.HexColor('#FBBF24')  # Yellow
        else:
            return colors.HexColor('#10B981')  # Green
    
    @staticmethod
    def _get_risk_color_for_level(level: str) -> colors.Color:
        """Get color based on risk level."""
        if level == "high":
            return colors.HexColor('#DC2626')
        elif level == "medium":
            return colors.HexColor('#F59E0B')
        else:
            return colors.HexColor('#10B981')
    
    @staticmethod
    def _get_risk_category(score: float) -> str:
        """Get risk category text."""
        if score >= 80:
            return "SEVERE RISK"
        elif score >= 51:
            return "HIGH RISK"
        elif score >= 21:
            return "MODERATE RISK"
        else:
            return "LOW RISK"
