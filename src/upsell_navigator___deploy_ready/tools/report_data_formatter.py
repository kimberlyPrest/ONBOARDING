from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any
import json

class ReportDataFormatterInput(BaseModel):
    """Input schema for ReportDataFormatter Tool."""
    report_data: Dict[str, Any] = Field(..., description="Dictionary containing all analysis results and metrics")
    live_name: str = Field(..., description="Name of the live stream for personalization")
    sales_result: str = Field(..., description="Sales result context for the report")

class ReportDataFormatterTool(BaseTool):
    """Tool for formatting live stream analysis data into professional Portuguese report text."""

    name: str = "ReportDataFormatter"
    description: str = (
        "Formats structured live stream analysis data into a comprehensive, professional Portuguese report text "
        "with proper section headers, bullet points, and formatting markers ready for DOCX conversion."
    )
    args_schema: Type[BaseModel] = ReportDataFormatterInput

    def _run(self, report_data: Dict[str, Any], live_name: str, sales_result: str) -> str:
        try:
            # Helper function to safely extract data
            def get_value(data, key, default="N/A"):
                return str(data.get(key, default)) if data.get(key) is not None else default
            
            # Helper function to format numbers
            def format_number(value, suffix=""):
                try:
                    if isinstance(value, (int, float)):
                        return f"{value:,.0f}{suffix}"
                    return str(value)
                except:
                    return str(value)
            
            # Helper function to format percentage
            def format_percentage(value):
                try:
                    if isinstance(value, (int, float)):
                        return f"{value:.1f}%"
                    return str(value)
                except:
                    return str(value)
            
            # Start building the formatted report
            report_text = f"""# RELATÓRIO DE ANÁLISE DA LIVE: {live_name.upper()}

## SUMÁRIO EXECUTIVO

Este relatório apresenta uma análise detalhada da performance da live "{live_name}", incluindo métricas de audiência, engajamento, qualidade dos dados e conversão. 

**Resultado de Vendas:** {sales_result}

---

## QUALIDADE DOS DADOS

### Métricas Gerais de Qualidade
"""
            
            # Data Quality Section
            quality_data = report_data.get("data_quality", {})
            if quality_data:
                report_text += f"""
• **Taxa de Completude dos Dados:** {format_percentage(quality_data.get("completeness_rate", "N/A"))}
• **Precisão das Métricas:** {get_value(quality_data, "accuracy_level")}
• **Cobertura Temporal:** {get_value(quality_data, "time_coverage")}
• **Integridade dos Timestamps:** {get_value(quality_data, "timestamp_integrity")}
"""
            else:
                report_text += "\n• Dados de qualidade não disponíveis no momento da análise.\n"

            # Audience and Retention Section
            report_text += """
---

## AUDIÊNCIA E RETENÇÃO

### Métricas de Audiência
"""
            
            audience_data = report_data.get("audience_metrics", {})
            if audience_data:
                report_text += f"""
• **Visualizações Totais:** {format_number(audience_data.get("total_views"))}
• **Pico de Audiência:** {format_number(audience_data.get("peak_viewers"))} espectadores
• **Média de Espectadores:** {format_number(audience_data.get("average_viewers"))} espectadores
• **Duração da Live:** {get_value(audience_data, "duration")}
• **Taxa de Retenção Média:** {format_percentage(audience_data.get("retention_rate"))}
"""
            else:
                report_text += "\n• Dados de audiência não disponíveis no momento da análise.\n"

            # Retention Analysis
            retention_data = report_data.get("retention_analysis", {})
            if retention_data:
                report_text += f"""
### Análise de Retenção
• **Retenção no Primeiro Minuto:** {format_percentage(retention_data.get("first_minute"))}
• **Retenção aos 5 Minutos:** {format_percentage(retention_data.get("five_minutes"))}
• **Retenção aos 15 Minutos:** {format_percentage(retention_data.get("fifteen_minutes"))}
• **Retenção até o Final:** {format_percentage(retention_data.get("completion_rate"))}
"""

            # Chat Engagement Section
            report_text += """
---

## ENGAJAMENTO DO CHAT

### Métricas de Interação
"""
            
            chat_data = report_data.get("chat_engagement", {})
            if chat_data:
                report_text += f"""
• **Total de Mensagens:** {format_number(chat_data.get("total_messages"))}
• **Usuários Únicos no Chat:** {format_number(chat_data.get("unique_users"))}
• **Mensagens por Minuto (Média):** {format_number(chat_data.get("messages_per_minute"))}
• **Taxa de Participação:** {format_percentage(chat_data.get("participation_rate"))}
• **Picos de Atividade:** {get_value(chat_data, "activity_peaks")}
"""
            else:
                report_text += "\n• Dados de engajamento do chat não disponíveis.\n"

            # Elite Pitch Section
            report_text += """
---

## PITCH DO ELITE

### Análise da Apresentação
"""
            
            pitch_data = report_data.get("pitch_analysis", {})
            if pitch_data:
                report_text += f"""
• **Momento do Pitch:** {get_value(pitch_data, "pitch_timing")}
• **Duração do Pitch:** {get_value(pitch_data, "pitch_duration")}
• **Retenção Durante o Pitch:** {format_percentage(pitch_data.get("retention_during_pitch"))}
• **Engajamento no Chat:** {get_value(pitch_data, "chat_response")}
• **Reações Principais:** {get_value(pitch_data, "main_reactions")}
"""
            else:
                report_text += "\n• Dados específicos do pitch não identificados na análise.\n"

            # Conversion vs Retention Section
            report_text += """
---

## CONVERSÃO VS. RETENÇÃO

### Correlação Entre Métricas
"""
            
            conversion_data = report_data.get("conversion_analysis", {})
            if conversion_data:
                report_text += f"""
• **Taxa de Conversão Estimada:** {format_percentage(conversion_data.get("conversion_rate"))}
• **Momento de Maior Conversão:** {get_value(conversion_data, "peak_conversion_time")}
• **Correlação Retenção-Conversão:** {get_value(conversion_data, "retention_correlation")}
• **Efetividade do Call-to-Action:** {get_value(conversion_data, "cta_effectiveness")}
"""
            else:
                report_text += "\n• Dados de conversão requerem análise adicional.\n"

            # Recommendations Section
            report_text += """
---

## RECOMENDAÇÕES

### Pontos de Melhoria Identificados
"""
            
            recommendations = report_data.get("recommendations", [])
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    report_text += f"• **{i}.** {rec}\n"
            else:
                # Generate basic recommendations based on available data
                report_text += """
• **Timing:** Avaliar os momentos de maior engajamento para otimizar futuras apresentações
• **Conteúdo:** Analisar os picos de atividade no chat para identificar tópicos de maior interesse
• **Retenção:** Implementar estratégias para melhorar a retenção nos primeiros minutos
• **Conversão:** Refinar o timing e a abordagem do pitch baseado nos dados de engajamento
"""

            # Attachments Section
            report_text += """
---

## ANEXOS

### Dados Técnicos Complementares
"""
            
            technical_data = report_data.get("technical_details", {})
            if technical_data:
                report_text += f"""
• **Plataforma de Streaming:** {get_value(technical_data, "platform")}
• **Qualidade de Transmissão:** {get_value(technical_data, "stream_quality")}
• **Ferramentas de Análise:** {get_value(technical_data, "analysis_tools")}
• **Período de Coleta:** {get_value(technical_data, "collection_period")}
"""
            else:
                report_text += """
• **Dados Brutos:** Disponíveis mediante solicitação
• **Metodologia:** Análise baseada em métricas de plataforma e engajamento
• **Limitações:** Algumas métricas podem apresentar variações devido à natureza dinâmica das lives
"""

            # Footer
            report_text += f"""

---

**Relatório gerado automaticamente para a live: {live_name}**
**Data de geração:** Processamento concluído
**Versão:** 1.0

*Este relatório foi formatado para conversão em documento DOCX e contém análise detalhada dos dados disponíveis.*
"""

            return report_text

        except Exception as e:
            return f"Erro ao formatar o relatório: {str(e)}. Verifique se os dados de entrada estão no formato correto."