export type Capability = {
  capability_id: string;
  label_zh: string;
  status: string;
  dependencies: string[];
  evidence: Array<{path: string; exists: boolean}>;
  evidence_complete: boolean;
  next_action: string;
  is_next_safe_action: boolean;
};

export type ResearchAsset = {
  asset_id: string;
  title: string;
  asset_type: string;
  source_path: string;
  review_state: string;
  provenance: string;
  categories: string[];
  mechanism_id?: string;
  mechanism_name?: string;
  exists: boolean;
};

export type FullCorpusProof = {
  version: string;
  job_id: string;
  status: string;
  corpus_inventory: {
    file_count: number;
    total_size_bytes: number;
    files: Array<{
      source_file: string;
      file_name: string;
      size_bytes: number;
    }>;
  };
  required_receipts: number;
  required_phases: string[];
  latest_validation: {
    status: string;
    valid: boolean;
    verified_receipts: number;
    required_receipts: number;
    promotion_allowed: boolean;
    validated_at?: string;
  } | null;
  promotion_readiness: {
    status: string;
    proof_verified: boolean;
    verified_receipts: number;
    required_receipts: number;
    promotion_allowed: boolean;
    next_required_action: string;
    forbidden_actions: string[];
  };
  promotion_allowed: boolean;
  commands: {
    pack: string;
    validate: string;
  };
};

export type PipelineFamily = {
  family: string;
  label: string;
  status: string;
  readiness_score: number;
  gap: string;
  next_safe_action: string;
  blocked_actions: string[];
  priority: number;
  is_next: boolean;
};

export type PipelineStage = {
  stage_id: string;
  label_zh: string;
  status: string;
  description: string;
};

export type PipelinePlan = {
  version: string;
  pipeline_id: string;
  project: string;
  mode: string;
  content_progression: string;
  target_family: PipelineFamily;
  stage_statuses: PipelineStage[];
  research_query: {
    asset_types: string[];
    categories: string[];
    review_state: string;
  };
  evidence_requirements: {
    minimum_items: number;
    structured_only: boolean;
    raw_corpus_allowed: boolean;
  };
  research_evidence: ResearchAsset[];
  schema_contract: {
    family: string;
    draft: string;
    path: string;
    payload_key: string;
    valid: boolean;
  };
  validation_gates: Array<{gate_id: string; description: string}>;
  agent_review_policy: {
    codex: string;
    antigravity: string;
    hermes: string;
    web_gpt: string;
  };
  owner_gate: {
    required: boolean;
    status: string;
  };
  forbidden_actions: string[];
  content_generation_allowed: boolean;
};

export type EvidencePack = {
  version: string;
  evidence_pack_id: string;
  pipeline_id: string;
  project: string;
  mode: string;
  content_progression: string;
  family: string;
  label: string;
  status: string;
  output_path: string;
  schema_contract: PipelinePlan['schema_contract'];
  research_query: PipelinePlan['research_query'];
  evidence_requirements: PipelinePlan['evidence_requirements'];
  evidence_summary: {
    item_count: number;
    source_paths: string[];
    structured_only: boolean;
    raw_corpus_allowed: boolean;
  };
  research_evidence: ResearchAsset[];
  validation_gates: PipelinePlan['validation_gates'];
  promotion_dependencies: {
    full_corpus_proof: {
      job_id: string;
      status: string;
      proof_verified: boolean;
      verified_receipts: number;
      required_receipts: number;
      promotion_allowed: boolean;
      next_required_action: string;
    };
  };
  agent_review_policy: PipelinePlan['agent_review_policy'];
  owner_gate: PipelinePlan['owner_gate'];
  blocked_actions: string[];
  content_generation_allowed: boolean;
  external_agent_execution_allowed: boolean;
};

export type EvidencePackMatrix = {
  version: string;
  matrix_id: string;
  pipeline_id: string;
  project: string;
  mode: string;
  content_progression: string;
  output_path: string;
  family_count: number;
  valid_family_count: number;
  invalid_families: string[];
  families: Record<string, {
    family: string;
    label: string;
    status: string;
    output_path: string;
    schema_path: string;
    evidence_item_count: number;
    validation_status: string;
    validation_error_count: number;
    content_generation_allowed: boolean;
    external_agent_execution_allowed: boolean;
    full_corpus_proof_status: string;
  }>;
  content_generation_allowed: boolean;
  external_agent_execution_allowed: boolean;
  owner_gate_required: boolean;
};

export type ArchitectureReconciliation = {
  version: string;
  source_context: {
    conversation_title: string;
    accepted_on: string;
    source_role: string;
  };
  fixed_identity: {
    short_name: string;
    principle: string;
    positioning_zh: string;
    not_a: string[];
    core_chain: string[];
  };
  architecture_layers: Array<{
    order: number;
    layer_id: string;
    label_zh: string;
    status: string;
    purpose: string;
    child_implementation: string | null;
  }>;
  experiment_calibration: {
    label_zh: string;
    status: string;
    scope: string;
    production_meaning: string;
  };
  implementation_alignment: {
    pipeline_version: string;
    pipeline_id: string;
    pipeline_layer: string;
    classification: string;
    next_family: string;
  };
  agent_role_contract: Array<{
    agent: string;
    status: string;
    display_status?: string;
    role: string;
    execution_boundary: string;
  }>;
  current_mismatch_report: Array<{
    mismatch_id: string;
    severity: string;
    summary: string;
    correction: string;
  }>;
  production_readiness: {
    system_mode: string;
    content_progression: string;
    owner_gate_required: boolean;
    owner_gate_status: string;
    content_generation_allowed: boolean;
    hermes_execution_status: string;
  };
  next_architecture_action: {
    action_id: string;
    label_zh: string;
    safe_command: string;
    blocked_actions: string[];
  };
};

export type StudioData = {
  control_plane: {
    version: string;
    locale: string;
    mode: string;
    content_progression: string;
    live_server_command: string;
  };
  antigravity_execution: {
    declared_mode: string;
    bridge_available: boolean;
    effective_state: string;
    can_dispatch_registered_reviews: boolean;
    blocked_reason: string | null;
    allowed_job_types: string[];
  };
  capability_roadmap: {
    version: string;
    mode: string;
    content_progression: string;
    capabilities: Capability[];
    next_safe_action: {
      capability_id: string;
      label_zh: string;
      action: string;
    };
  };
  research_asset_catalog: {
    catalog_name: string;
    version: string;
    source_of_truth: string[];
    items: ResearchAsset[];
    summary: {
      total_indexed: number;
      returned: number;
      by_type: Record<string, number>;
    };
    guardrails: string[];
  };
  full_corpus_proof: FullCorpusProof;
  creation_schema_registry: {
    registry_name: string;
    version: string;
    draft: string;
    common_schema: string;
    families: Array<{
      family: string;
      title: string;
      path: string;
      valid: boolean;
      payload_key: string;
    }>;
    summary: {
      family_count: number;
      all_schemas_valid: boolean;
    };
  };
  safe_action_catalog: {
    actions: Array<{
      action_id: string;
      label_zh: string;
      method: string;
      path: string;
    }>;
    forbidden_actions: string[];
  };
  architecture_reconciliation: ArchitectureReconciliation;
  corpus_pipeline: {
    version: string;
    pipeline_id: string;
    mode: string;
    content_progression: string;
    project: string;
    stages: PipelineStage[];
    families: PipelineFamily[];
    next_family: PipelineFamily;
    forbidden_actions: string[];
    next_plan: PipelinePlan;
    next_evidence_pack: EvidencePack;
    evidence_pack_matrix: EvidencePackMatrix;
  };
  system_identity: {
    name: string;
    positioning: string;
    not_a: string[];
    core_chain: string[];
  };
  current_project: {
    project_name: string;
    selected_project: string;
    current_phase: string;
    current_subphase: string;
    phase_status: string;
    system_mode: string;
    content_progression: string;
    last_completed_mission: string;
  };
  agent_panel: {
    items: Array<{
      agent: string;
      status: string;
      display_status?: string;
      mode: string;
      can_execute: boolean;
      role: string;
    }>;
  };
  artifact_map: {
    items: Array<{area: string; status: string; note: string}>;
  };
  creation_coverage_matrix: {
    assessment: string;
    items: Array<{
      asset: string;
      status: string;
      gap: string;
      asset_id?: string;
      readiness_score?: number;
    }>;
  };
  creation_asset_registry: {
    registry_name: string;
    version: string;
    project: string;
    mode: string;
    source_of_truth: string[];
    asset_families: Array<{
      asset_id: string;
      label: string;
      status: string;
      readiness_score: number;
      why_not_complete: string;
      known_support: string[];
      missing_capabilities: string[];
      source_artifacts: string[];
      next_safe_action: string;
      blocked_actions: string[];
    }>;
    coverage_summary: {
      total: number;
      by_status: Record<string, number>;
      complete: number;
      lowest_readiness: number;
      highest_readiness: number;
    };
    guardrails: string[];
    next_safe_action: string;
  };
  runtime_status: {
    health_commands: string[];
    state_validity_command: string;
    status_command: string;
    studio_data_command: string;
    current_mission: string;
    responsible_agent: string;
    registry_status: string;
    adapter_modes: Record<string, {mode: string; can_execute: boolean}>;
    handoff_attempts: unknown[];
    expected_outputs: string[];
    blocked_actions: string[];
  };
  next_safe_action: {
    recommended: string;
    runtime_command: string;
    blocked_next_action: string;
    safe_commands: string[];
  };
  owner_gate: {
    required: boolean;
    status: string;
    review_status: string;
    authorization_scope: string[];
    forbidden_scope: string[];
    decision_boundary: string;
    expires_after_mission: string;
  };
};
