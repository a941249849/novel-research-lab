import {useEffect, useMemo, useState} from 'react';
import {Theme} from '@astryxdesign/core';
import {AppShell} from '@astryxdesign/core/AppShell';
import {Banner} from '@astryxdesign/core/Banner';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {Grid} from '@astryxdesign/core/Grid';
import {Heading} from '@astryxdesign/core/Heading';
import {
  Layout,
  LayoutContent,
  LayoutHeader,
} from '@astryxdesign/core/Layout';
import {List, ListItem} from '@astryxdesign/core/List';
import {MetadataList, MetadataListItem} from '@astryxdesign/core/MetadataList';
import {Section} from '@astryxdesign/core/Section';
import {
  SideNav,
  SideNavHeading,
  SideNavItem,
  SideNavSection,
} from '@astryxdesign/core/SideNav';
import {HStack, VStack} from '@astryxdesign/core/Stack';
import {StatusDot} from '@astryxdesign/core/StatusDot';
import {Table, pixel, proportional} from '@astryxdesign/core/Table';
import {Text} from '@astryxdesign/core/Text';
import {TextInput} from '@astryxdesign/core/TextInput';
import {Token} from '@astryxdesign/core/Token';
import {neutralTheme} from '@astryxdesign/theme-neutral/built';
import type {StudioData} from './types';

declare global {
  interface Window {
    __NRL_STUDIO_DATA__?: StudioData;
  }
}

type ViewID = 'overview' | 'architecture' | 'research' | 'creation' | 'pipeline' | 'agents' | 'runtime';
type TableRow = Record<string, unknown> & {id: string};

const EMPTY_DATA = {
  control_plane: {
    version: '0.2',
    locale: 'zh-CN',
    mode: 'UNKNOWN_MODE',
    content_progression: 'UNKNOWN',
    live_server_command: 'python3 system/runtime/nrl.py studio-serve --port 4173',
  },
  capability_roadmap: {
    version: '0.2',
    mode: 'UNKNOWN_MODE',
    content_progression: 'UNKNOWN',
    capabilities: [],
    next_safe_action: {capability_id: 'unknown', label_zh: '等待数据', action: '运行 studio-build。'},
  },
  research_asset_catalog: {
    catalog_name: 'NRL Research Asset Catalog',
    version: '0.2',
    source_of_truth: [],
    items: [],
    summary: {total_indexed: 0, returned: 0, by_type: {}},
    guardrails: [],
  },
  full_corpus_proof: {
    version: '0.8',
    job_id: 'job-v08-full-corpus-proof-review',
    status: 'blocked_on_proof_verification',
    corpus_inventory: {file_count: 0, total_size_bytes: 0, files: []},
    required_receipts: 0,
    required_phases: [],
    latest_validation: null,
    promotion_readiness: {
      status: 'blocked_on_proof_verification',
      proof_verified: false,
      verified_receipts: 0,
      required_receipts: 0,
      promotion_allowed: false,
      next_required_action: '',
      forbidden_actions: [],
    },
    promotion_allowed: false,
    commands: {
      pack: 'python3 system/runtime/nrl.py full-corpus-proof-pack --all',
      validate: 'python3 system/runtime/nrl.py full-corpus-proof-validate --file <path>',
    },
  },
  creation_schema_registry: {
    registry_name: 'NRL Creation Schema Registry',
    version: '0.2',
    draft: 'Draft-07',
    common_schema: '',
    families: [],
    summary: {family_count: 0, all_schemas_valid: false},
  },
  safe_action_catalog: {actions: [], forbidden_actions: []},
  architecture_reconciliation: {
    version: '0.4',
    source_context: {
      conversation_title: '',
      accepted_on: '',
      source_role: '',
    },
    fixed_identity: {
      short_name: 'Novel Research Lab',
      principle: 'Corpus-to-Creation',
      positioning_zh: '基于中文热门长篇小说语料研究蒸馏的原创长篇小说创作引擎',
      not_a: [],
      core_chain: [],
    },
    architecture_layers: [],
    experiment_calibration: {
      label_zh: 'Core7 小批量试验',
      status: 'accepted_as_calibration_basis',
      scope: '',
      production_meaning: '',
    },
    implementation_alignment: {
      pipeline_version: '0.3',
      pipeline_id: 'corpus-to-creation',
      pipeline_layer: 'planning_pipeline',
      classification: '',
      next_family: '',
    },
    agent_role_contract: [],
    current_mismatch_report: [],
    production_readiness: {
      system_mode: 'UNKNOWN_MODE',
      content_progression: 'UNKNOWN',
      owner_gate_required: true,
      owner_gate_status: 'UNKNOWN',
      content_generation_allowed: false,
      hermes_execution_status: 'paused_not_removed',
    },
    next_architecture_action: {
      action_id: 'architecture_reconciliation_v0_4',
      label_zh: '锁定系统架构并把 v0.3 归位为规划管线层',
      safe_command: 'python3 system/runtime/nrl.py architecture-status',
      blocked_actions: [],
    },
  },
  corpus_pipeline: {
    version: '0.3',
    pipeline_id: 'corpus-to-creation',
    mode: 'UNKNOWN_MODE',
    content_progression: 'UNKNOWN',
    project: 'UNKNOWN_PROJECT',
    stages: [],
    families: [],
    next_family: {family: 'unknown', label: 'Unknown', status: 'missing', readiness_score: 0, gap: '', next_safe_action: '', blocked_actions: [], priority: 0, is_next: true},
    forbidden_actions: [],
    next_plan: {
      version: '0.3',
      pipeline_id: 'corpus-to-creation-unknown',
      project: 'UNKNOWN_PROJECT',
      mode: 'UNKNOWN_MODE',
      content_progression: 'UNKNOWN',
      target_family: {family: 'unknown', label: 'Unknown', status: 'missing', readiness_score: 0, gap: '', next_safe_action: '', blocked_actions: [], priority: 0, is_next: true},
      stage_statuses: [],
      research_query: {asset_types: [], categories: [], review_state: ''},
      evidence_requirements: {minimum_items: 0, structured_only: true, raw_corpus_allowed: false},
      research_evidence: [],
      schema_contract: {family: 'unknown', draft: '', path: '', payload_key: '', valid: false},
      validation_gates: [],
      agent_review_policy: {codex: '', antigravity: '', hermes: '', web_gpt: ''},
      owner_gate: {required: true, status: 'UNKNOWN'},
      forbidden_actions: [],
      content_generation_allowed: false,
    },
  },
  system_identity: {name: 'Novel Research Lab', positioning: 'Corpus-to-Creation', not_a: [], core_chain: []},
  current_project: {
    project_name: 'Novel Research Lab',
    selected_project: 'UNKNOWN_PROJECT',
    current_phase: 'UNKNOWN_PHASE',
    current_subphase: '',
    phase_status: 'UNKNOWN',
    system_mode: 'UNKNOWN_MODE',
    content_progression: 'UNKNOWN',
    last_completed_mission: '',
  },
  agent_panel: {items: []},
  artifact_map: {items: []},
  creation_coverage_matrix: {assessment: '', items: []},
  creation_asset_registry: {
    registry_name: 'Creation Asset Registry',
    version: '0.1',
    project: 'UNKNOWN_PROJECT',
    mode: 'UNKNOWN_MODE',
    source_of_truth: [],
    asset_families: [],
    coverage_summary: {total: 0, by_status: {}, complete: 0, lowest_readiness: 0, highest_readiness: 0},
    guardrails: [],
    next_safe_action: '',
  },
  runtime_status: {
    health_commands: [],
    state_validity_command: '',
    status_command: '',
    studio_data_command: '',
    current_mission: '',
    responsible_agent: '',
    registry_status: '',
    adapter_modes: {},
    handoff_attempts: [],
    expected_outputs: [],
    blocked_actions: [],
  },
  next_safe_action: {recommended: '', runtime_command: '', blocked_next_action: '', safe_commands: []},
  owner_gate: {
    required: false,
    status: 'UNKNOWN',
    review_status: 'UNKNOWN',
    authorization_scope: [],
    forbidden_scope: [],
    decision_boundary: '',
    expires_after_mission: '',
  },
} satisfies StudioData;

const viewLabels: Record<ViewID, {label: string; subtitle: string; icon: 'info' | 'search' | 'viewColumns' | 'wrench' | 'warning'}> = {
  overview: {label: '系统总览', subtitle: '能力、状态与下一动作', icon: 'info'},
  architecture: {label: '系统架构', subtitle: '源架构、Core7 校准与 v0.3 归位', icon: 'info'},
  research: {label: '研究资产', subtitle: 'Phase 1 结构化研究目录', icon: 'search'},
  creation: {label: '创作资产', subtitle: '九类资产覆盖与契约', icon: 'viewColumns'},
  pipeline: {label: '生成管线', subtitle: 'Planning Pipeline layer · v0.3', icon: 'wrench'},
  agents: {label: 'Agent 与任务', subtitle: '角色、适配器与任务边界', icon: 'wrench'},
  runtime: {label: '运行状态与 Owner Gate', subtitle: '体检、门禁与阻塞动作', icon: 'warning'},
};

const statusNames: Record<string, string> = {
  missing: '缺失',
  contract_ready: '契约就绪',
  data_ready: '数据就绪',
  runnable: '可运行',
  blocked: '已阻塞',
  partial: '部分覆盖',
  partial_data: '数据部分完成',
  partial_engine: '引擎部分可用',
  protected_input: '受保护输入',
  seed: '种子状态',
  accepted_as_calibration_basis: '已接受为校准依据',
  formal: '已审核',
  stub: '占位资产',
  candidate_retained: '候选保留',
  promoted: '已提升',
  candidate: '候选',
  local: '本地执行',
  manual_handoff: '人工交接',
  review_received_pending_owner_gate: '等待 Owner Gate',
  asset_layer_present: '资产层已存在',
  research_asset: '研究资产',
  completed: '已完成',
  prepared: '已准备',
  schema_validation: 'Schema 校验',
  source_evidence: '来源证据',
  reference_integrity: '引用完整性',
  naming_collision: '命名冲突',
  lifecycle_transition: '生命周期',
  owner_gate: 'Owner Gate',
  proof_gate_ready: '证明门已就绪',
  proof_verified: '证明已验证',
  verified_not_promoted: '已验证未提升',
  blocked_on_owner_gate: 'Owner Gate 阻塞',
  blocked_on_proof_verification: '等待证明验证',
};

function statusColor(status: string) {
  if (status.includes('blocked') || status.includes('missing') || status.includes('REQUIRED')) return 'red';
  if (status.includes('partial') || status.includes('pending') || status.includes('manual')) return 'orange';
  if (status.includes('seed') || status.includes('contract')) return 'yellow';
  if (status.includes('runnable') || status.includes('ready') || status.includes('verified') || status.includes('PASS') || status === 'formal') return 'green';
  return 'gray';
}

function StatusToken({status}: {status: string}) {
  return <Token label={statusNames[status] || status} color={statusColor(status)} size="sm" />;
}

function PageHeader({view}: {view: ViewID}) {
  return (
    <LayoutHeader hasDivider height={72}>
      <Section padding={4}>
        <VStack gap={0.5}>
          <Heading level={2}>{viewLabels[view].label}</Heading>
          <Text type="supporting">{viewLabels[view].subtitle}</Text>
        </VStack>
      </Section>
    </LayoutHeader>
  );
}

function SummaryCard({label, value, status}: {label: string; value: string; status?: string}) {
  return (
    <Card padding={3}>
      <VStack gap={1}>
        <Text type="supporting" display="block">{label}</Text>
        <Heading level={3}>{value}</Heading>
        {status ? <StatusToken status={status} /> : null}
      </VStack>
    </Card>
  );
}

const artifactNotes: Record<string, string> = {
  Corpus: '语料层已建立，Studio 不直接访问原始小说文本。',
  Mechanisms: '跨书机制库已形成并可通过研究资产目录查询。',
  'Grand Synthesis': '综合研究资产用于支撑 Corpus-to-Creation。',
  'Story Bible': '当前原创项目的故事圣经。',
  'Outline Tree': 'Phase 2D 大纲树资产。',
  'Planning Pack': 'Phase 2E 受控规划资产。',
  'Validation Reports': 'Codex 工程与一致性验证结果。',
  'Review Reports': 'Antigravity 人工文学审查结果。',
  'State Ledger': '已有基础 Schema，尚未形成完整长篇状态账本。',
};

function OverviewView({data, compact}: {data: StudioData; compact: boolean}) {
  const capabilityRows: TableRow[] = data.capability_roadmap.capabilities.map((item) => ({
    id: item.capability_id,
    capability: item.label_zh,
    status: statusNames[item.status] || item.status,
    evidence: `${item.evidence.filter((entry) => entry.exists).length}/${item.evidence.length}`,
    next: item.next_action,
  }));
  return (
    <Section padding={5}>
      <VStack gap={5}>
        <Grid columns={{minWidth: 220, max: 4, repeat: 'fit'}} gap={3}>
          <SummaryCard label="当前项目" value={data.current_project.selected_project} />
          <SummaryCard label="当前阶段" value={data.current_project.current_phase} status={data.current_project.phase_status} />
          <SummaryCard label="系统模式" value={data.control_plane.mode} />
          <SummaryCard label="内容推进" value="Owner Gate 冻结" status="blocked" />
        </Grid>
        <Grid columns={{minWidth: 220, max: 4, repeat: 'fit'}} gap={3}>
          <SummaryCard
            label="全量语料"
            value={`${data.full_corpus_proof.corpus_inventory.file_count} 本`}
            status={data.full_corpus_proof.status}
          />
          <SummaryCard
            label="阅读证明"
            value={`${data.full_corpus_proof.promotion_readiness.verified_receipts}/${data.full_corpus_proof.promotion_readiness.required_receipts}`}
            status={data.full_corpus_proof.latest_validation?.status || data.full_corpus_proof.promotion_readiness.status}
          />
          <SummaryCard
            label="提升状态"
            value={data.full_corpus_proof.promotion_readiness.promotion_allowed ? '允许提升' : '未提升'}
            status={data.full_corpus_proof.promotion_readiness.status}
          />
          <SummaryCard
            label="正文生产"
            value="禁止"
            status="blocked"
          />
        </Grid>
        <Banner
          status={data.full_corpus_proof.promotion_readiness.proof_verified ? 'success' : 'warning'}
          title="全量小说集阅读证明"
          description={`${data.full_corpus_proof.promotion_readiness.verified_receipts}/${data.full_corpus_proof.promotion_readiness.required_receipts} 条证明已验证；${data.full_corpus_proof.promotion_readiness.next_required_action}`}
        />
        <Banner
          status="info"
          title={`下一安全动作：${data.capability_roadmap.next_safe_action.label_zh}`}
          description={data.capability_roadmap.next_safe_action.action}
        />
        <VStack gap={2}>
          <HStack gap={2} vAlign="center">
            <Heading level={3}>系统能力路线图</Heading>
            <Token label={`${capabilityRows.length} 项能力`} color="blue" size="sm" />
          </HStack>
          {compact ? (
            <List density="compact" hasDividers>
              {data.capability_roadmap.capabilities.map((item) => (
                <ListItem
                  key={item.capability_id}
                  label={item.label_zh}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.next_action}</Text>}
                  endContent={<StatusToken status={item.status} />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={capabilityRows}
              idKey="id"
              density="compact"
              dividers="rows"
              hasHover
              textOverflow="wrap"
              columns={[
                {key: 'capability', header: '能力', width: proportional(1)},
                {key: 'status', header: '状态', width: pixel(120)},
                {key: 'evidence', header: '证据', width: pixel(80)},
                {key: 'next', header: '系统动作', width: proportional(2)},
              ]}
            />
          )}
        </VStack>
        <VStack gap={2}>
          <Heading level={3}>产物地图</Heading>
          <List density="compact" hasDividers>
            {data.artifact_map.items.map((item) => (
              <ListItem
                key={item.area}
                label={item.area}
                description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{artifactNotes[item.area] || item.note}</Text>}
                endContent={<StatusToken status={item.status} />}
              />
            ))}
          </List>
        </VStack>
      </VStack>
    </Section>
  );
}

function ArchitectureView({data, compact}: {data: StudioData; compact: boolean}) {
  const architecture = data.architecture_reconciliation;
  const layerRows: TableRow[] = architecture.architecture_layers.map((layer) => ({
    id: layer.layer_id,
    order: layer.order,
    layer: layer.label_zh,
    status: statusNames[layer.status] || layer.status,
    child: layer.child_implementation || '无',
    purpose: layer.purpose,
  }));
  const agentRows: TableRow[] = architecture.agent_role_contract.map((item) => ({
    id: item.agent,
    agent: item.agent,
    status: item.display_status || item.status,
    role: item.role,
    boundary: item.execution_boundary,
  }));

  return (
    <Section padding={5}>
      <VStack gap={5}>
        <Banner
          status="info"
          title={`${architecture.fixed_identity.short_name} / ${architecture.fixed_identity.principle}`}
          description={architecture.fixed_identity.positioning_zh}
        />
        <Grid columns={{minWidth: 220, max: 4, repeat: 'fit'}} gap={3}>
          <SummaryCard label="架构版本" value={architecture.version} />
          <SummaryCard label="校准依据" value={architecture.experiment_calibration.label_zh} status={architecture.experiment_calibration.status} />
          <SummaryCard label="v0.3 归位" value={architecture.implementation_alignment.pipeline_layer} />
          <SummaryCard label="Owner Gate" value={architecture.production_readiness.owner_gate_status} status="blocked" />
        </Grid>
        <VStack gap={2}>
          <HStack gap={2} vAlign="center" wrap="wrap">
            <Heading level={3}>Corpus-to-Creation 链路</Heading>
            <Token label={architecture.source_context.conversation_title || 'source context'} color="blue" size="sm" />
          </HStack>
          <List density="compact" hasDividers>
            {architecture.fixed_identity.core_chain.map((item) => (
              <ListItem key={item} label={item} />
            ))}
          </List>
        </VStack>
        <VStack gap={2}>
          <HStack gap={2} vAlign="center" wrap="wrap">
            <Heading level={3}>十层系统架构</Heading>
            <Token label={architecture.implementation_alignment.classification} color="teal" size="sm" />
          </HStack>
          {compact ? (
            <List density="compact" hasDividers>
              {architecture.architecture_layers.map((layer) => (
                <ListItem
                  key={layer.layer_id}
                  label={`${layer.order}. ${layer.label_zh}`}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{layer.purpose}</Text>}
                  endContent={<StatusToken status={layer.status} />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={layerRows}
              idKey="id"
              density="compact"
              dividers="rows"
              hasHover
              textOverflow="wrap"
              columns={[
                {key: 'order', header: '#', width: pixel(56)},
                {key: 'layer', header: '架构层', width: proportional(1)},
                {key: 'status', header: '状态', width: pixel(140)},
                {key: 'child', header: '子实现', width: pixel(190)},
                {key: 'purpose', header: '职责', width: proportional(2)},
              ]}
            />
          )}
        </VStack>
        <Grid columns={{minWidth: 300, max: 2, repeat: 'fit'}} gap={4}>
          <VStack gap={2}>
            <Heading level={3}>Core7 小批量试验</Heading>
            <MetadataList columns="single">
              <MetadataListItem label="状态">{statusNames[architecture.experiment_calibration.status] || architecture.experiment_calibration.status}</MetadataListItem>
              <MetadataListItem label="范围">{architecture.experiment_calibration.scope}</MetadataListItem>
              <MetadataListItem label="生产含义">{architecture.experiment_calibration.production_meaning}</MetadataListItem>
            </MetadataList>
          </VStack>
          <VStack gap={2}>
            <Heading level={3}>下一架构动作</Heading>
            <MetadataList columns="single">
              <MetadataListItem label="动作">{architecture.next_architecture_action.label_zh}</MetadataListItem>
              <MetadataListItem label="命令">{architecture.next_architecture_action.safe_command}</MetadataListItem>
              <MetadataListItem label="Hermes">{`Hermes: ${architecture.production_readiness.hermes_execution_status}`}</MetadataListItem>
            </MetadataList>
          </VStack>
        </Grid>
        <Banner
          status="warning"
          title="当前偏差修正"
          description={architecture.current_mismatch_report.map((item) => `${item.summary} ${item.correction}`).join(' ')}
        />
        <VStack gap={2}>
          <Heading level={3}>Agent 角色边界</Heading>
          {compact ? (
            <List density="compact" hasDividers>
              {architecture.agent_role_contract.map((item) => (
                <ListItem
                  key={item.agent}
                  label={`${item.agent}: ${item.display_status || item.status}`}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.role}</Text>}
                />
              ))}
            </List>
          ) : (
            <Table
              data={agentRows}
              idKey="id"
              density="compact"
              dividers="rows"
              hasHover
              textOverflow="wrap"
              columns={[
                {key: 'agent', header: 'Agent', width: pixel(150)},
                {key: 'status', header: '状态', width: pixel(220)},
                {key: 'role', header: '职责', width: proportional(1)},
                {key: 'boundary', header: '边界', width: proportional(1)},
              ]}
            />
          )}
        </VStack>
      </VStack>
    </Section>
  );
}

function ResearchView({data, compact}: {data: StudioData; compact: boolean}) {
  const [query, setQuery] = useState('');
  const filtered = useMemo(
    () => data.research_asset_catalog.items.filter((item) =>
      `${item.title} ${item.asset_type} ${item.mechanism_name || ''} ${item.categories.join(' ')}`
        .toLowerCase()
        .includes(query.toLowerCase()),
    ),
    [data.research_asset_catalog.items, query],
  );
  const rows: TableRow[] = filtered.map((item) => ({
    id: item.asset_id,
    title: item.title,
    type: item.asset_type,
    state: statusNames[item.review_state] || item.review_state,
    provenance: statusNames[item.provenance] || item.provenance,
    source: item.source_path,
  }));
  return (
    <Section padding={5}>
      <VStack gap={4}>
        <Banner
          status={data.full_corpus_proof.promotion_readiness.proof_verified ? 'success' : 'warning'}
          title="全量小说集阅读证明已进入研究资产目录"
          description={`${data.full_corpus_proof.corpus_inventory.file_count} 本语料，${data.full_corpus_proof.promotion_readiness.verified_receipts}/${data.full_corpus_proof.promotion_readiness.required_receipts} 条证明；状态为 ${statusNames[data.full_corpus_proof.promotion_readiness.status] || data.full_corpus_proof.promotion_readiness.status}。`}
          endContent={<StatusToken status={data.full_corpus_proof.latest_validation?.status || data.full_corpus_proof.promotion_readiness.status} />}
        />
        <HStack gap={3} wrap="wrap" vAlign="end">
          <TextInput
            label="筛选研究资产"
            value={query}
            onChange={setQuery}
            placeholder="小说、资产类型、机制名称或分类"
            hasClear
            size="sm"
          />
          <Token label={`已索引 ${data.research_asset_catalog.summary.total_indexed}`} color="blue" />
          <Token label={`当前 ${rows.length}`} color="teal" />
        </HStack>
        {compact ? (
          <List density="compact" hasDividers>
            {filtered.map((item) => (
              <ListItem
                key={item.asset_id}
                label={`${item.title} · ${item.mechanism_name || item.asset_type}`}
                description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.source_path}</Text>}
                endContent={<StatusToken status={item.review_state} />}
              />
            ))}
          </List>
        ) : (
          <Table
            data={rows}
            idKey="id"
            density="compact"
            dividers="rows"
            isStriped
            hasHover
            textOverflow="truncate"
            columns={[
              {key: 'title', header: '来源作品', width: pixel(140)},
              {key: 'type', header: '资产类型', width: pixel(150)},
              {key: 'state', header: '审核状态', width: pixel(110)},
              {key: 'provenance', header: '资产层级', width: pixel(110)},
              {key: 'source', header: '来源路径', width: proportional(2)},
            ]}
          />
        )}
        <Banner
          status="info"
          title="研究目录只消费结构化衍生资产"
          description="原始小说语料不会通过 Studio 或 research-assets 暴露。"
        />
      </VStack>
    </Section>
  );
}

function CreationView({data, compact}: {data: StudioData; compact: boolean}) {
  const coverageRows: TableRow[] = data.creation_coverage_matrix.items.map((item) => ({
    id: item.asset_id || item.asset,
    family: item.asset,
    status: statusNames[item.status] || item.status,
    readiness: item.readiness_score ?? 0,
    gap: item.gap,
  }));
  const schemaRows: TableRow[] = data.creation_schema_registry.families.map((item) => ({
    id: item.family,
    family: item.family,
    title: item.title,
    payload: item.payload_key,
    valid: item.valid ? '通过' : '失败',
    path: item.path,
  }));
  return (
    <Section padding={5}>
      <VStack gap={5}>
        <VStack gap={2}>
          <HStack gap={2} vAlign="center" wrap="wrap">
            <Heading level={3}>创作覆盖矩阵 / Creation Coverage Matrix</Heading>
            <StatusToken status={data.creation_asset_registry.coverage_summary.complete ? 'complete' : 'partial'} />
          </HStack>
          {compact ? (
            <List density="compact" hasDividers>
              {data.creation_coverage_matrix.items.map((item) => (
                <ListItem
                  key={item.asset_id || item.asset}
                  label={`${item.asset} · 就绪度 ${item.readiness_score ?? 0}`}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.gap}</Text>}
                  endContent={<StatusToken status={item.status} />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={coverageRows}
              idKey="id"
              density="compact"
              dividers="rows"
              hasHover
              textOverflow="wrap"
              columns={[
                {key: 'family', header: '资产家族', width: pixel(150)},
                {key: 'status', header: '覆盖状态', width: pixel(110)},
                {key: 'readiness', header: '就绪度', width: pixel(80)},
                {key: 'gap', header: '当前缺口', width: proportional(3)},
              ]}
            />
          )}
        </VStack>
        <VStack gap={2}>
          <HStack gap={2} vAlign="center" wrap="wrap">
            <Heading level={3}>Draft-07 Schema 契约</Heading>
            <StatusToken status={data.creation_schema_registry.summary.all_schemas_valid ? 'runnable' : 'blocked'} />
          </HStack>
          {compact ? (
            <List density="compact" hasDividers>
              {data.creation_schema_registry.families.map((item) => (
                <ListItem
                  key={item.family}
                  label={item.title}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.path}</Text>}
                  endContent={<StatusToken status={item.valid ? 'runnable' : 'blocked'} />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={schemaRows}
              idKey="id"
              density="compact"
              dividers="rows"
              isStriped
              textOverflow="truncate"
              columns={[
                {key: 'family', header: 'Family ID', width: pixel(150)},
                {key: 'title', header: '契约', width: proportional(1)},
                {key: 'payload', header: 'Payload', width: pixel(150)},
                {key: 'valid', header: '验证', width: pixel(80)},
                {key: 'path', header: 'Schema 路径', width: proportional(2)},
              ]}
            />
          )}
        </VStack>
        <Banner
          status="warning"
          title="契约就绪不等于内容完成"
          description="当前项目资产库保持为空；禁止自动生成完整人物卡、NPC、势力、招式、命名词典和正文。"
        />
      </VStack>
    </Section>
  );
}

function PipelineView({data, compact}: {data: StudioData; compact: boolean}) {
  const stageRows: TableRow[] = data.corpus_pipeline.stages.map((item) => ({
    id: item.stage_id,
    stage: item.label_zh,
    status: statusNames[item.status] || item.status,
    description: item.description,
  }));
  const familyRows: TableRow[] = data.corpus_pipeline.families.map((item) => ({
    id: item.family,
    family: item.label,
    status: statusNames[item.status] || item.status,
    readiness: item.readiness_score,
    next: item.next_safe_action,
  }));
  const plan = data.corpus_pipeline.next_plan;
  const gateRows: TableRow[] = plan.validation_gates.map((item) => ({
    id: item.gate_id,
    gate: statusNames[item.gate_id] || item.gate_id,
    description: item.description,
  }));
  return (
    <Section padding={5}>
      <VStack gap={5}>
        <Banner
          status="info"
          title={`Corpus-to-Creation Pipeline：下一资产家族 ${data.corpus_pipeline.next_family.label}`}
          description={data.corpus_pipeline.next_family.next_safe_action}
          endContent={<StatusToken status={data.corpus_pipeline.next_family.status} />}
        />
        <Grid columns={{minWidth: 220, max: 4, repeat: 'fit'}} gap={3}>
          <SummaryCard label="目标 Family" value={plan.target_family.family} status={plan.target_family.status} />
          <SummaryCard label="就绪度" value={String(plan.target_family.readiness_score)} />
          <SummaryCard label="Schema" value={plan.schema_contract.payload_key} status={plan.schema_contract.valid ? 'runnable' : 'blocked'} />
          <SummaryCard label="内容生成" value={plan.content_generation_allowed ? '允许' : '禁止'} status={plan.content_generation_allowed ? 'runnable' : 'blocked'} />
        </Grid>
        <VStack gap={2}>
          <HStack gap={2} vAlign="center" wrap="wrap">
            <Heading level={3}>管线阶段</Heading>
            <Token label={data.corpus_pipeline.pipeline_id} color="blue" size="sm" />
          </HStack>
          {compact ? (
            <List density="compact" hasDividers>
              {data.corpus_pipeline.stages.map((item) => (
                <ListItem
                  key={item.stage_id}
                  label={item.label_zh}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.description}</Text>}
                  endContent={<StatusToken status={item.status} />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={stageRows}
              idKey="id"
              density="compact"
              dividers="rows"
              hasHover
              textOverflow="wrap"
              columns={[
                {key: 'stage', header: '阶段', width: pixel(170)},
                {key: 'status', header: '状态', width: pixel(110)},
                {key: 'description', header: '说明', width: proportional(3)},
              ]}
            />
          )}
        </VStack>
        <VStack gap={2}>
          <Heading level={3}>资产构建顺序</Heading>
          {compact ? (
            <List density="compact" hasDividers>
              {data.corpus_pipeline.families.map((item) => (
                <ListItem
                  key={item.family}
                  label={`${item.label} · ${item.readiness_score}`}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.next_safe_action}</Text>}
                  endContent={<StatusToken status={item.status} />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={familyRows}
              idKey="id"
              density="compact"
              dividers="rows"
              isStriped
              hasHover
              textOverflow="wrap"
              columns={[
                {key: 'family', header: 'Family', width: pixel(150)},
                {key: 'status', header: '状态', width: pixel(110)},
                {key: 'readiness', header: '就绪度', width: pixel(80)},
                {key: 'next', header: '下一动作', width: proportional(3)},
              ]}
            />
          )}
        </VStack>
        <Grid columns={{minWidth: 300, max: 2, repeat: 'fit'}} gap={4}>
          <VStack gap={2}>
            <Heading level={3}>证据需求</Heading>
            <MetadataList columns="single">
              <MetadataListItem label="Asset Types">{plan.research_query.asset_types.join(', ')}</MetadataListItem>
              <MetadataListItem label="Mechanism Categories">{plan.research_query.categories.join(', ')}</MetadataListItem>
              <MetadataListItem label="Schema Path">{plan.schema_contract.path}</MetadataListItem>
              <MetadataListItem label="Research Evidence">{String(plan.research_evidence.length)}</MetadataListItem>
            </MetadataList>
          </VStack>
          <VStack gap={2}>
            <Heading level={3}>禁止动作</Heading>
            <List density="compact" hasDividers>
              {plan.forbidden_actions.map((item) => (
                <ListItem key={item} label={item} endContent={<StatusToken status="blocked" />} />
              ))}
            </List>
          </VStack>
        </Grid>
        <VStack gap={2}>
          <Heading level={3}>校验门禁</Heading>
          {compact ? (
            <List density="compact" hasDividers>
              {plan.validation_gates.map((item) => (
                <ListItem
                  key={item.gate_id}
                  label={statusNames[item.gate_id] || item.gate_id}
                  description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{item.description}</Text>}
                  endContent={<StatusToken status="runnable" />}
                />
              ))}
            </List>
          ) : (
            <Table
              data={gateRows}
              idKey="id"
              density="compact"
              dividers="rows"
              textOverflow="wrap"
              columns={[
                {key: 'gate', header: 'Gate', width: pixel(160)},
                {key: 'description', header: '约束', width: proportional(3)},
              ]}
            />
          )}
        </VStack>
      </VStack>
    </Section>
  );
}

const roleNames: Record<string, string> = {
  Codex: '本地运行时、工程实现、验证与编排',
  Antigravity: '人工外部文学审查',
  Hermes: '暂停但未移除；授权后承担写作与文学增强',
  'Web GPT': '架构审查，不负责派发任务',
  Owner: '阶段和能力变更的最终门禁',
};

function AgentsView({data}: {data: StudioData}) {
  return (
    <Section padding={5}>
      <VStack gap={4}>
        <List density="compact" hasDividers>
          {data.agent_panel.items.map((item) => (
            <ListItem
              key={item.agent}
              label={item.agent}
              description={<Text type="supporting" display="block" textWrap="wrap" wordBreak="break-word">{roleNames[item.agent] || item.role}</Text>}
              startContent={<StatusDot variant={item.can_execute ? 'success' : 'warning'} label={`${item.agent} 状态`} />}
              endContent={<HStack gap={1}><StatusToken status={item.mode} /><StatusToken status={item.display_status || item.status} /></HStack>}
            />
          ))}
        </List>
        <MetadataList columns="multi">
          <MetadataListItem label="当前任务">{data.runtime_status.current_mission}</MetadataListItem>
          <MetadataListItem label="责任 Agent">{data.runtime_status.responsible_agent}</MetadataListItem>
          <MetadataListItem label="任务注册状态">{data.runtime_status.registry_status}</MetadataListItem>
          <MetadataListItem label="预期产物">{data.runtime_status.expected_outputs.join(', ') || '无'}</MetadataListItem>
        </MetadataList>
        <Banner
          status="info"
          title="客户端协作边界"
          description="Studio 不直接调用 Hermes 或 Antigravity；没有真实适配器时继续使用 manual_handoff。"
        />
      </VStack>
    </Section>
  );
}

function RuntimeView({data, live}: {data: StudioData; live: boolean}) {
  const [actionResult, setActionResult] = useState<{ok: boolean; message: string} | null>(null);
  async function runAction(path: string) {
    try {
      const response = await fetch(path, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: '{}',
      });
      const payload = await response.json();
      setActionResult({
        ok: response.ok && (payload.passed ?? payload.valid ?? true),
        message: response.ok ? JSON.stringify(payload) : payload.error || '操作失败',
      });
    } catch {
      setActionResult({ok: false, message: '动态服务不可用，请使用 studio-serve 启动。'});
    }
  }
  return (
    <Section padding={5}>
      <VStack gap={5}>
        <HStack gap={2} wrap="wrap">
          {data.safe_action_catalog.actions.map((action) => (
            <Button
              key={action.action_id}
              label={action.label_zh}
              variant={action.action_id === 'system-check' ? 'primary' : 'secondary'}
              size="sm"
              isDisabled={!live}
              tooltip={!live ? '请通过 studio-serve 启动动态控制台' : undefined}
              clickAction={() => runAction(action.path)}
            />
          ))}
          <StatusToken status={live ? 'runnable' : 'blocked'} />
        </HStack>
        {actionResult ? (
          <Banner
            status={actionResult.ok ? 'success' : 'error'}
            title={actionResult.ok ? '系统检查通过' : '系统检查失败'}
            description={actionResult.message}
          />
        ) : null}
        <Grid columns={{minWidth: 320, max: 2, repeat: 'fit'}} gap={4}>
          <MetadataList columns="single">
            <MetadataListItem label="Owner Gate 必需">{String(data.owner_gate.required)}</MetadataListItem>
            <MetadataListItem label="Owner Gate 状态">{data.owner_gate.status}</MetadataListItem>
            <MetadataListItem label="审查状态">{data.owner_gate.review_status}</MetadataListItem>
            <MetadataListItem label="决策边界">{data.owner_gate.decision_boundary}</MetadataListItem>
            <MetadataListItem label="授权有效期">{data.owner_gate.expires_after_mission}</MetadataListItem>
          </MetadataList>
          <VStack gap={3}>
            <Heading level={3}>阻塞动作</Heading>
            <List density="compact" hasDividers>
              {data.runtime_status.blocked_actions.map((item) => (
                <ListItem key={item} label={item} endContent={<StatusToken status="blocked" />} />
              ))}
            </List>
          </VStack>
        </Grid>
        <VStack gap={2}>
          <Heading level={3}>运行命令</Heading>
          <List density="compact" hasDividers>
            {data.runtime_status.health_commands.map((command) => (
              <ListItem
                key={command}
                label="运行命令"
                description={<Text type="code" display="block" textWrap="wrap" wordBreak="break-word">{command}</Text>}
                endContent={<Token label="只读/验证" color="teal" size="sm" />}
              />
            ))}
          </List>
        </VStack>
      </VStack>
    </Section>
  );
}

function App() {
  const [data, setData] = useState<StudioData>(() => window.__NRL_STUDIO_DATA__ || EMPTY_DATA);
  const [view, setView] = useState<ViewID>('overview');
  const [live, setLive] = useState(false);
  const [compact, setCompact] = useState(() => window.matchMedia('(max-width: 720px)').matches);

  useEffect(() => {
    fetch('/api/studio-data')
      .then((response) => {
        if (!response.ok) throw new Error('live API unavailable');
        return response.json();
      })
      .then((nextData: StudioData) => {
        setData(nextData);
        setLive(true);
      })
      .catch(() => setLive(false));
  }, []);

  useEffect(() => {
    const media = window.matchMedia('(max-width: 720px)');
    const update = () => setCompact(media.matches);
    media.addEventListener('change', update);
    return () => media.removeEventListener('change', update);
  }, []);

  const sideNav = (
    <SideNav
      header={
        <SideNavHeading
          superheading="NRL Control Plane"
          heading="Novel Research Lab"
          subheading={`v${data.control_plane.version} · 中文`}
          headerEndContent={<StatusDot variant={live ? 'success' : 'warning'} label={live ? '动态服务' : '静态快照'} />}
        />
      }
      collapsible={{defaultIsCollapsed: false, buttonLabel: '收起导航'}}
      footer={
        <SideNavSection title="系统边界">
          <SideNavItem label="Owner Gate 生效" icon="warning" isDisabled />
          <SideNavItem label="Hermes 已暂停" icon="stop" isDisabled />
        </SideNavSection>
      }
    >
      <SideNavSection title="控制台">
        {(Object.keys(viewLabels) as ViewID[]).map((item) => (
          <SideNavItem
            key={item}
            label={viewLabels[item].label}
            icon={viewLabels[item].icon}
            isSelected={view === item}
            href={`#${item}`}
            onClick={(event) => {
              event.preventDefault();
              setView(item);
            }}
          />
        ))}
      </SideNavSection>
    </SideNav>
  );

  const content = view === 'overview'
    ? <OverviewView data={data} compact={compact} />
    : view === 'architecture'
      ? <ArchitectureView data={data} compact={compact} />
      : view === 'research'
        ? <ResearchView data={data} compact={compact} />
        : view === 'creation'
          ? <CreationView data={data} compact={compact} />
          : view === 'pipeline'
            ? <PipelineView data={data} compact={compact} />
            : view === 'agents'
              ? <AgentsView data={data} />
              : <RuntimeView data={data} live={live} />;

  return (
    <Theme theme={neutralTheme}>
      <AppShell
        sideNav={sideNav}
        banner={
          <Banner
            status="warning"
            container="section"
            title="Phase 2E Owner Gate 等待确认"
            description="内容推进保持冻结；当前只允许系统硬化、状态读取和验证。"
            endContent={<Token label="内容冻结" color="red" size="sm" />}
          />
        }
        contentPadding={0}
        height="fill"
        variant="section"
      >
        <Layout
          height="fill"
          header={<PageHeader view={view} />}
          content={<LayoutContent label={viewLabels[view].label}>{content}</LayoutContent>}
        />
      </AppShell>
    </Theme>
  );
}

export default App;
