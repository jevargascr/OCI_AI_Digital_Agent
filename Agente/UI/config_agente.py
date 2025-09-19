# 1. Importaciones
from typing import Dict
from oci.addons.adk import Agent, AgentClient, tool
from oci.addons.adk.tool.prebuilt import AgenticRagTool
import random

# 1. Definiciones del agente
client = AgentClient(
    auth_type="api_key",
    profile="DEFAULT",
    region="us-chicago-1",
)

knowledge_base_id = "ocid1.genaiagentknowledgebase.oc1.us-chicago-1.amaaaaaaixhtvjaa2xrehahf7sr4rxuxph2mvgw3svh3bshtnpqswn46vdjq"
rag_tool = AgenticRagTool(
    name="Running RAG tool",
    description="Retrieve authoritative answers to customer FAQs about the bank's products, fees, eligibility, processes, service channels, and policies from the bank's knowledge base.",
    knowledge_base_ids=[knowledge_base_id],
)

# Create a local agent object with the client, instructions, and tools
# You also need agent endpoint id. To obtain that, follow Step 1
agent = Agent(
    client=client,
    agent_endpoint_id="ocid1.genaiagentendpoint.oc1.us-chicago-1.amaaaaaaixhtvjaaen3nvmr3vfpbjb33o4lvhzdmi5k5mromlnardmmkf32q",
    instructions="""You are a banking virtual assistant. Always use the RAG tool as your primary and authoritative source to answer customer FAQs about the bank's products, fees, eligibility, processes (open/apply/cancel), digital channels, hours, and policies.
                    - Language: with a professional and friendly tone.
                    - Accuracy: prefer the most recent documents; when dates or validity are present, state them. Do not invent information.
                    - When uncertain: if confidence is low or the answer is not in the knowledge base, say so clearly and provide official contact options (e.g., website, call center).
                    - Safety: never ask for or process sensitive data (account/card numbers, PIN/CVV, passwords, OTP). Do not access or imply access to personal accounts.
                    - Scope: do not provide personalized financial advice or guarantee approvals.
                    - Style: be concise; use short bullet points for lists and numbered steps for procedures.""",

    tools=[rag_tool]
)

# Ejecutar setup cada vez
# Sincroniza el agente local (definido en Python) con el recurso remoto de Oracle Cloud Infrastructure (OCI).
#if __name__ == "__main__":
try:
    agent.setup()
except Exception as e:
    print(f"Error al sincronizar el agente con OCI: {e}")
