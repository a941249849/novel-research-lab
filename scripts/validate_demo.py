#!/usr/bin/env python3
import os
import json
import sys

# Configuration
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_DIR = os.path.join(WORKSPACE_DIR, 'demo_run')

def validate_book_dna(data):
    errors = []
    # Check required fields
    for field in ["book_title", "author", "level_system", "world_lore"]:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            
    # Check level_system
    if "level_system" in data:
        ls = data["level_system"]
        if not isinstance(ls, dict) or "level_stages" not in ls:
            errors.append("level_system must be an object containing level_stages")
        elif not isinstance(ls["level_stages"], list) or len(ls["level_stages"]) == 0:
            errors.append("level_stages must be a non-empty array")
        elif not all(isinstance(x, str) for x in ls["level_stages"]):
            errors.append("All items in level_stages must be strings")
            
    # Check zero_sum_constraints
    if "zero_sum_constraints" in data:
        zsc = data["zero_sum_constraints"]
        if not isinstance(zsc, list):
            errors.append("zero_sum_constraints must be an array")
        else:
            for idx, item in enumerate(zsc):
                if not isinstance(item, dict):
                    errors.append(f"zero_sum_constraints[{idx}] must be an object")
                    continue
                if "asset_name" not in item or "max_global_slots" not in item:
                    errors.append(f"zero_sum_constraints[{idx}] missing asset_name or max_global_slots")
                elif not isinstance(item["max_global_slots"], int) or item["max_global_slots"] < 1:
                    errors.append(f"zero_sum_constraints[{idx}].max_global_slots must be an integer >= 1")
                    
    # Check world_lore
    if "world_lore" in data:
        wl = data["world_lore"]
        if not isinstance(wl, dict) or "core_description" not in wl:
            errors.append("world_lore must be an object containing core_description")
        elif not isinstance(wl["core_description"], str):
            errors.append("world_lore.core_description must be a string")
            
    return len(errors) == 0, errors

def validate_narrative_dna(data):
    errors = []
    if "plot_checkpoints" not in data:
        errors.append("Missing required field: plot_checkpoints")
    elif not isinstance(data["plot_checkpoints"], list):
        errors.append("plot_checkpoints must be an array")
    else:
        for idx, item in enumerate(data["plot_checkpoints"]):
            if not isinstance(item, dict):
                errors.append(f"plot_checkpoints[{idx}] must be an object")
                continue
            for field in ["node_id", "title", "tension"]:
                if field not in item:
                    errors.append(f"plot_checkpoints[{idx}] missing required field: {field}")
            if "tension" in item:
                t = item["tension"]
                if not isinstance(t, int) or t < -10 or t > 10:
                    errors.append(f"plot_checkpoints[{idx}].tension must be an integer between -10 and 10")
            if "is_combat_skippable" in item and not isinstance(item["is_combat_skippable"], bool):
                errors.append(f"plot_checkpoints[{idx}].is_combat_skippable must be a boolean")
                
    return len(errors) == 0, errors

def validate_state_ledger(data):
    errors = []
    # Check required fields
    for field in ["true_profile", "public_mask", "inventory", "faction_reputation"]:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            
    # Check true_profile
    if "true_profile" in data:
        tp = data["true_profile"]
        if not isinstance(tp, dict):
            errors.append("true_profile must be an object")
        else:
            for field in ["actor_id", "name", "level"]:
                if field not in tp:
                    errors.append(f"true_profile missing required field: {field}")
            if "moral_threshold" in tp:
                m = tp["moral_threshold"]
                if not isinstance(m, int) or m < 0 or m > 100:
                    errors.append("true_profile.moral_threshold must be an integer 0-100")
            if "utility_priority" in tp:
                u = tp["utility_priority"]
                if not isinstance(u, (int, float)) or u < 0.0 or u > 1.0:
                    errors.append("true_profile.utility_priority must be a float 0.0-1.0")
            if "symbiotic_entities" in tp:
                se = tp["symbiotic_entities"]
                if not isinstance(se, list):
                    errors.append("true_profile.symbiotic_entities must be an array")
                else:
                    for s_idx, entity in enumerate(se):
                        if not isinstance(entity, dict) or "name" not in entity:
                            errors.append(f"true_profile.symbiotic_entities[{s_idx}] must contain name")
                            
    # Check public_mask
    if "public_mask" in data:
        pm = data["public_mask"]
        if not isinstance(pm, dict) or "is_mask_active" not in pm:
            errors.append("public_mask must be an object containing is_mask_active")
        elif not isinstance(pm["is_mask_active"], bool):
            errors.append("public_mask.is_mask_active must be a boolean")
            
    # Check inventory
    if "inventory" in data:
        inv = data["inventory"]
        if not isinstance(inv, list):
            errors.append("inventory must be an array")
        else:
            for idx, item in enumerate(inv):
                if not isinstance(item, dict):
                    errors.append(f"inventory[{idx}] must be an object")
                    continue
                for field in ["item_name", "item_type"]:
                    if field not in item:
                        errors.append(f"inventory[{idx}] missing required field: {field}")
                        
    # Check faction_reputation
    if "faction_reputation" in data:
        fr = data["faction_reputation"]
        if not isinstance(fr, dict):
            errors.append("faction_reputation must be an object")
        else:
            for k, v in fr.items():
                if not isinstance(v, int) or v < -100 or v > 100:
                    errors.append(f"faction_reputation['{k}'] value must be an integer between -100 and 100")
                    
    return len(errors) == 0, errors

def validate_audit_report(data):
    errors = []
    # Check required fields
    for field in ["audit_timestamp", "originality_metrics", "compliance_status", "violation_flags", "consistency_status"]:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            
    # Check originality_metrics
    if "originality_metrics" in data:
        om = data["originality_metrics"]
        if not isinstance(om, dict):
            errors.append("originality_metrics must be an object")
        else:
            for field in ["originality_score", "similarity_detected_percentage", "disclaimer_applied"]:
                if field not in om:
                    errors.append(f"originality_metrics missing required field: {field}")
            if "originality_score" in om:
                s = om["originality_score"]
                if not isinstance(s, (int, float)) or s < 0.0 or s > 1.0:
                    errors.append("originality_score must be a float 0.0-1.0")
            if "disclaimer_applied" in om and not isinstance(om["disclaimer_applied"], bool):
                errors.append("disclaimer_applied must be a boolean")
                
    # Check compliance_status
    if "compliance_status" in data:
        c = data["compliance_status"]
        if c not in ["passed", "warnings", "failed"]:
            errors.append("compliance_status must be passed, warnings, or failed")
            
    # Check violation_flags
    if "violation_flags" in data:
        vf = data["violation_flags"]
        if not isinstance(vf, list):
            errors.append("violation_flags must be an array")
        else:
            for idx, flag in enumerate(vf):
                if not isinstance(flag, dict):
                    errors.append(f"violation_flags[{idx}] must be an object")
                    continue
                for field in ["severity", "rule_violated", "detected_pattern"]:
                    if field not in flag:
                        errors.append(f"violation_flags[{idx}] missing required field: {field}")
                        
    # Check consistency_status
    if "consistency_status" in data:
        cs = data["consistency_status"]
        if not isinstance(cs, dict):
            errors.append("consistency_status must be an object")
        else:
            for field in ["level_consistency", "inventory_backlash_enforced", "reputation_conflict_detected"]:
                if field not in cs:
                    errors.append(f"consistency_status missing required field: {field}")
                elif not isinstance(cs[field], bool):
                    errors.append(f"consistency_status.{field} must be a boolean")
                    
    return len(errors) == 0, errors

validation_targets = [
    {
        "file": "output_original_setting.json",
        "validator": validate_book_dna
    },
    {
        "file": "output_original_outline.json",
        "validator": validate_narrative_dna
    },
    {
        "file": "output_state_ledger.json",
        "validator": validate_state_ledger
    },
    {
        "file": "output_audit_report.json",
        "validator": validate_audit_report
    }
]

def check_validation():
    success = True
    for target in validation_targets:
        filepath = os.path.join(DEMO_DIR, target["file"])
        print(f"Validating {target['file']}...")
        
        if not os.path.exists(filepath):
            print(f"  Error: Target file {filepath} not found.")
            success = False
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"  Error parsing JSON: {str(e)}")
                success = False
                continue
                
        is_valid, errors = target["validator"](data)
        if is_valid:
            print(f"  Success: {target['file']} is VALID.")
        else:
            print(f"  ValidationError: {target['file']} failed validation.")
            for err in errors:
                print(f"    - {err}")
            success = False
            
    if success:
        print("\nAll JSON files successfully validated against Phase 0B v1.0 standard rules.")
        sys.exit(0)
    else:
        print("\nSome JSON files failed validation.")
        sys.exit(1)

if __name__ == '__main__':
    check_validation()
