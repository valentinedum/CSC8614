# TP5/test_finalize_intents.py
"""Test finalize avec différents intents forcés (pour le rapport)"""
import uuid

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState
from TP5.agent.nodes.finalize import finalize
from TP5.agent.logger import log_event

if __name__ == "__main__":
    emails = load_all_emails()
    
    # Test 1: ESCALATE (E07 - risque données sensibles)
    print("=" * 60)
    print("TEST 1: ESCALATE (E07)")
    print("=" * 60)
    e = emails[6]
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )
    # Forcer l'intent escalate
    state.decision.intent = "escalate"
    state.decision.risk_level = "high"
    state.decision.rationale = "Demande de données personnelles sensibles (PII)"
    
    state = finalize(state)
    
    print("final_kind =", state.final_kind)
    print("final_text =", state.final_text)
    print("\n=== HANDOFF PACKET ===")
    for action in state.actions:
        if action["type"] == "handoff_packet":
            print(f"  run_id: {action['run_id']}")
            print(f"  email_id: {action['email_id']}")
            print(f"  summary: {action['summary']}")
            print(f"  evidence_ids: {action['evidence_ids']}")
    
    # Test 2: IGNORE (E08 - phishing)
    print("\n" + "=" * 60)
    print("TEST 2: IGNORE (E08)")
    print("=" * 60)
    e = emails[7]
    state2 = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )
    # Forcer l'intent ignore
    state2.decision.intent = "ignore"
    state2.decision.risk_level = "high"
    state2.decision.rationale = "Email de phishing détecté (domaine suspect, urgence artificielle)"
    
    state2 = finalize(state2)
    
    print("final_kind =", state2.final_kind)
    print("final_text =", state2.final_text)
    
    # Test 3: ASK_CLARIFICATION (E06 - ambigu)
    print("\n" + "=" * 60)
    print("TEST 3: ASK_CLARIFICATION (E06)")
    print("=" * 60)
    e = emails[5]
    state3 = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )
    # Forcer l'intent ask_clarification
    state3.decision.intent = "ask_clarification"
    state3.decision.rationale = "Email trop vague - fichier et deadline non précisés"
    
    state3 = finalize(state3)
    
    print("final_kind =", state3.final_kind)
    print("final_text =", state3.final_text)
    
    print("\n" + "=" * 60)
    print("Vérifiez les JSONL dans TP5/runs/ pour les événements finalize")
    print("=" * 60)
