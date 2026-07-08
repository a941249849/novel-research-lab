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

export type StudioData = {
  control_plane: {
    version: string;
    locale: string;
    mode: string;
    content_progression: string;
    live_server_command: string;
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
