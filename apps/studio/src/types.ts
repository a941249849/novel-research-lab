export type StudioData = {
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
    items: Array<{
      area: string;
      status: string;
      note: string;
    }>;
  };
  creation_coverage_matrix: {
    assessment: string;
    items: Array<{
      asset: string;
      status: string;
      gap: string;
    }>;
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
