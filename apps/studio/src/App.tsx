import {useEffect, useState} from 'react';
import {Theme} from '@astryxdesign/core';
import {AppShell} from '@astryxdesign/core/AppShell';
import {Badge} from '@astryxdesign/core/Badge';
import {Card} from '@astryxdesign/core/Card';
import {Grid} from '@astryxdesign/core/Grid';
import {Heading} from '@astryxdesign/core/Heading';
import {List, ListItem} from '@astryxdesign/core/List';
import {MetadataList, MetadataListItem} from '@astryxdesign/core/MetadataList';
import {Section} from '@astryxdesign/core/Section';
import {HStack, VStack} from '@astryxdesign/core/Stack';
import {StatusDot} from '@astryxdesign/core/StatusDot';
import {Text} from '@astryxdesign/core/Text';
import {Token} from '@astryxdesign/core/Token';
import {neutralTheme} from '@astryxdesign/theme-neutral/built';
import type {StudioData} from './types';

declare global {
  interface Window {
    __NRL_STUDIO_DATA__?: StudioData;
  }
}

const fallbackData: StudioData = {
  system_identity: {
    name: 'Novel Research Lab',
    positioning: 'Corpus-to-Creation engine for Chinese long-form web novel creation.',
    not_a: ['generic AI writing app', 'InkOS clone', 'document pipeline'],
    core_chain: ['corpus reading', 'mechanism distillation', 'original project synthesis', 'review', 'state ledger'],
  },
  current_project: {
    project_name: 'Novel Research Lab',
    selected_project: 'UNKNOWN_PROJECT',
    current_phase: 'UNKNOWN_PHASE',
    current_subphase: 'UNKNOWN_SUBPHASE',
    phase_status: 'UNKNOWN_STATUS',
    system_mode: 'UNKNOWN_MODE',
    content_progression: 'UNKNOWN_PROGRESSION',
    last_completed_mission: '',
  },
  agent_panel: {items: []},
  artifact_map: {items: []},
  creation_coverage_matrix: {assessment: 'Coverage unavailable.', items: []},
  runtime_status: {
    state_validity_command: 'python3 system/runtime/nrl.py validate-state',
    status_command: 'python3 system/runtime/nrl.py system-status',
    studio_data_command: 'python3 system/runtime/nrl.py studio-data',
    current_mission: 'UNKNOWN_MISSION',
    responsible_agent: 'unknown',
    registry_status: 'unknown',
    adapter_modes: {},
    handoff_attempts: [],
    expected_outputs: [],
    blocked_actions: [],
  },
  next_safe_action: {
    recommended: 'Build Studio data before inspecting this shell.',
    runtime_command: 'python3 system/runtime/nrl.py studio-data',
    blocked_next_action: 'No content action available from fallback data.',
    safe_commands: [],
  },
  owner_gate: {
    required: false,
    status: 'UNKNOWN',
    review_status: 'UNKNOWN',
    authorization_scope: [],
    forbidden_scope: [],
    decision_boundary: 'Unknown',
    expires_after_mission: 'Unknown',
  },
};

function statusToken(status: string) {
  const normalized = status.toLowerCase();
  if (normalized.includes('missing') || normalized.includes('blocked') || normalized.includes('required')) {
    return 'red';
  }
  if (normalized.includes('partial') || normalized.includes('pending') || normalized.includes('warning')) {
    return 'orange';
  }
  if (normalized.includes('seed') || normalized.includes('prepared')) {
    return 'yellow';
  }
  if (normalized.includes('pass') || normalized.includes('complete') || normalized.includes('local')) {
    return 'green';
  }
  return 'gray';
}

function SectionTitle({title, subtitle}: {title: string; subtitle?: string}) {
  return (
    <VStack gap={1}>
      <Heading level={2}>{title}</Heading>
      {subtitle ? (
        <Text type="supporting" display="block">
          {subtitle}
        </Text>
      ) : null}
    </VStack>
  );
}

function TokenRow({items}: {items: string[]}) {
  return (
    <HStack gap={1} wrap="wrap">
      {items.map((item) => (
        <Token key={item} label={item} color={statusToken(item)} size="sm" />
      ))}
    </HStack>
  );
}

function CurrentProject({data}: {data: StudioData}) {
  const project = data.current_project;
  return (
    <Section padding={5} dividers={['bottom']}>
      <VStack gap={4}>
        <SectionTitle title="Current Project" subtitle="The active project remains frozen at the current Owner Gate sample state." />
        <Grid columns={{minWidth: 220, max: 4, repeat: 'fit'}} gap={3}>
          <Card padding={4}>
            <Text type="supporting" display="block">Project</Text>
            <Heading level={3}>{project.selected_project}</Heading>
          </Card>
          <Card padding={4}>
            <Text type="supporting" display="block">Phase</Text>
            <Heading level={3}>{project.current_phase}</Heading>
            <Text type="supporting" display="block">{project.current_subphase}</Text>
          </Card>
          <Card padding={4}>
            <Text type="supporting" display="block">System Mode</Text>
            <Heading level={3}>{project.system_mode}</Heading>
          </Card>
          <Card padding={4}>
            <Text type="supporting" display="block">Content Progression</Text>
            <Heading level={3}>{project.content_progression}</Heading>
          </Card>
        </Grid>
        <MetadataList columns="multi">
          <MetadataListItem label="Phase status">{project.phase_status}</MetadataListItem>
          <MetadataListItem label="Last completed mission">{project.last_completed_mission || 'No completed mission recorded'}</MetadataListItem>
        </MetadataList>
      </VStack>
    </Section>
  );
}

function SystemIdentity({data}: {data: StudioData}) {
  return (
    <Section padding={5} variant="muted" dividers={['bottom']}>
      <VStack gap={4}>
        <HStack gap={4} wrap="wrap" vAlign="center">
          <VStack gap={1}>
            <Heading level={1}>{data.system_identity.name}</Heading>
            <Text type="large" display="block">{data.system_identity.positioning}</Text>
          </VStack>
          <Badge variant="info" label="Read-only Studio v0.1" />
        </HStack>
        <Grid columns={{minWidth: 260, max: 2, repeat: 'fit'}} gap={4}>
          <List header={<Heading level={3}>Not This</Heading>} density="compact" hasDividers>
            {data.system_identity.not_a.map((item) => (
              <ListItem key={item} label={item} endContent={<Token label="not_a" color="gray" size="sm" />} />
            ))}
          </List>
          <List header={<Heading level={3}>Corpus-to-Creation Chain</Heading>} density="compact" hasDividers>
            {data.system_identity.core_chain.map((item, index) => (
              <ListItem key={item} label={item} endContent={<Token label={`step ${index + 1}`} color="blue" size="sm" />} />
            ))}
          </List>
        </Grid>
      </VStack>
    </Section>
  );
}

function AgentPanel({data}: {data: StudioData}) {
  return (
    <Section padding={5} dividers={['bottom']}>
      <VStack gap={4}>
        <SectionTitle title="Agent Panel" subtitle="Roles are explicit. Studio does not call Hermes or Antigravity." />
        <Grid columns={{minWidth: 260, max: 5, repeat: 'fit'}} gap={3}>
          {data.agent_panel.items.map((item) => (
            <Card key={item.agent} padding={4}>
              <VStack gap={2}>
                <HStack gap={2} vAlign="center">
                  <StatusDot variant={item.can_execute ? 'success' : 'warning'} label={`${item.agent} execution status`} />
                  <Heading level={3}>{item.agent}</Heading>
                </HStack>
                <Token label={item.display_status || item.status} color={statusToken(item.status)} size="sm" />
                <Text type="supporting" display="block">{item.mode}</Text>
                <Text display="block">{item.role}</Text>
              </VStack>
            </Card>
          ))}
        </Grid>
      </VStack>
    </Section>
  );
}

function ArtifactMap({data}: {data: StudioData}) {
  return (
    <Section padding={5} dividers={['bottom']}>
      <VStack gap={4}>
        <SectionTitle title="Artifact Map" subtitle="The map shows product-relevant assets, not raw corpus access." />
        <List density="compact" hasDividers>
          {data.artifact_map.items.map((item) => (
            <ListItem
              key={item.area}
              label={item.area}
              description={item.note}
              endContent={<Token label={item.status} color={statusToken(item.status)} size="sm" />}
            />
          ))}
        </List>
      </VStack>
    </Section>
  );
}

function CreationCoverageMatrix({data}: {data: StudioData}) {
  return (
    <Section padding={5} dividers={['bottom']}>
      <VStack gap={4}>
        <SectionTitle title="Creation Coverage Matrix" subtitle={data.creation_coverage_matrix.assessment} />
        <Grid columns={{minWidth: 280, max: 3, repeat: 'fit'}} gap={3}>
          {data.creation_coverage_matrix.items.map((item) => (
            <Card key={item.asset} padding={4} variant="muted">
              <VStack gap={2}>
                <HStack gap={2} vAlign="center">
                  <Heading level={3}>{item.asset}</Heading>
                  <Token label={item.status} color={statusToken(item.status)} size="sm" />
                </HStack>
                <Text type="supporting" display="block">{item.gap}</Text>
              </VStack>
            </Card>
          ))}
        </Grid>
      </VStack>
    </Section>
  );
}

function RuntimeStatus({data}: {data: StudioData}) {
  const adapterRows = Object.entries(data.runtime_status.adapter_modes).map(([agent, adapter]) => ({
    agent,
    mode: adapter.mode,
    canExecute: String(adapter.can_execute),
  }));
  return (
    <Section padding={5} dividers={['bottom']}>
      <VStack gap={4}>
        <SectionTitle title="Runtime Status" subtitle="Runtime reads are allowed; mutations still go through explicit commands and gates." />
        <Grid columns={{minWidth: 300, max: 2, repeat: 'fit'}} gap={4}>
          <MetadataList columns="single">
            <MetadataListItem label="Current mission">{data.runtime_status.current_mission}</MetadataListItem>
            <MetadataListItem label="Responsible agent">{data.runtime_status.responsible_agent}</MetadataListItem>
            <MetadataListItem label="Registry status">{data.runtime_status.registry_status}</MetadataListItem>
            <MetadataListItem label="State command">{data.runtime_status.state_validity_command}</MetadataListItem>
            <MetadataListItem label="Studio data command">{data.runtime_status.studio_data_command}</MetadataListItem>
          </MetadataList>
          <List header={<Heading level={3}>Adapter Modes</Heading>} density="compact" hasDividers>
            {adapterRows.map((row) => (
              <ListItem
                key={row.agent}
                label={row.agent}
                description={row.mode}
                endContent={<Token label={row.canExecute === 'true' ? 'can_execute' : 'manual'} color={row.canExecute === 'true' ? 'green' : 'orange'} size="sm" />}
              />
            ))}
          </List>
        </Grid>
        <VStack gap={2}>
          <Heading level={3}>Blocked Actions</Heading>
          <TokenRow items={data.runtime_status.blocked_actions} />
        </VStack>
        <VStack gap={2}>
          <Heading level={3}>Expected Outputs</Heading>
          <TokenRow items={data.runtime_status.expected_outputs.length ? data.runtime_status.expected_outputs : ['no expected output registered']} />
        </VStack>
      </VStack>
    </Section>
  );
}

function NextSafeAction({data}: {data: StudioData}) {
  return (
    <Section padding={5} variant="muted" dividers={['bottom']}>
      <VStack gap={4}>
        <SectionTitle title="Next Safe Action" subtitle={data.next_safe_action.recommended} />
        <Badge variant="warning" label={data.next_safe_action.blocked_next_action} />
        <List header={<Heading level={3}>Safe Commands</Heading>} density="compact" hasDividers>
          {data.next_safe_action.safe_commands.map((command) => (
            <ListItem key={command} label={command} endContent={<Token label="read-only" color="teal" size="sm" />} />
          ))}
        </List>
      </VStack>
    </Section>
  );
}

function OwnerGate({data}: {data: StudioData}) {
  return (
    <Section padding={5}>
      <VStack gap={4}>
        <SectionTitle title="Owner Gate" subtitle="The Owner remains the authority for any content or capability transition." />
        <Grid columns={{minWidth: 280, max: 2, repeat: 'fit'}} gap={4}>
          <MetadataList columns="single">
            <MetadataListItem label="Required">{String(data.owner_gate.required)}</MetadataListItem>
            <MetadataListItem label="Status">{data.owner_gate.status}</MetadataListItem>
            <MetadataListItem label="Review status">{data.owner_gate.review_status}</MetadataListItem>
            <MetadataListItem label="Decision boundary">{data.owner_gate.decision_boundary}</MetadataListItem>
            <MetadataListItem label="Expires">{data.owner_gate.expires_after_mission}</MetadataListItem>
          </MetadataList>
          <VStack gap={3}>
            <VStack gap={2}>
              <Heading level={3}>Authorization Scope</Heading>
              <TokenRow items={data.owner_gate.authorization_scope} />
            </VStack>
            <VStack gap={2}>
              <Heading level={3}>Forbidden Scope</Heading>
              <TokenRow items={data.owner_gate.forbidden_scope} />
            </VStack>
          </VStack>
        </Grid>
      </VStack>
    </Section>
  );
}

function App() {
  const [data, setData] = useState<StudioData>(() => window.__NRL_STUDIO_DATA__ || fallbackData);

  useEffect(() => {
    if (window.__NRL_STUDIO_DATA__) {
      return;
    }
    fetch('/nrl-studio-data.json')
      .then((response) => (response.ok ? response.json() : fallbackData))
      .then((nextData: StudioData) => setData(nextData))
      .catch(() => setData(fallbackData));
  }, []);

  return (
    <Theme theme={neutralTheme}>
      <AppShell contentPadding={0} height="auto" variant="surface">
        <VStack gap={0}>
          <SystemIdentity data={data} />
          <CurrentProject data={data} />
          <AgentPanel data={data} />
          <ArtifactMap data={data} />
          <CreationCoverageMatrix data={data} />
          <RuntimeStatus data={data} />
          <NextSafeAction data={data} />
          <OwnerGate data={data} />
        </VStack>
      </AppShell>
    </Theme>
  );
}

export default App;
