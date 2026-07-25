#!/usr/bin/env node
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const [requestPath, sourcePath, model] = process.argv.slice(2);
if (!requestPath || !sourcePath || !model) process.exit(2);
const sdkPath = path.join(os.homedir(), ".config/opencode/node_modules/@opencode-ai/sdk/dist/index.js");
const { createOpencode } = await import(pathToFileURL(sdkPath).href);
const directory = process.cwd();
const [request, source] = await Promise.all([fs.readFile(requestPath, "utf8"), fs.readFile(sourcePath, "utf8")]);
const abort = new AbortController();
const timer = setTimeout(() => abort.abort(), 10 * 60 * 1000);
const { client, server } = await createOpencode({ signal: abort.signal });
try {
  const created = await client.session.create({ query: { directory }, body: { title: `NRL direct deep read: ${path.basename(sourcePath)}` }, throwOnError: true });
  const session = created.data;
  await client.session.promptAsync({
    path: { id: session.id }, query: { directory }, throwOnError: true,
    body: {
      model: { providerID: "opencode-go", modelID: model }, agent: "build",
      system: "Read the complete source text in the user message. Do not use tools. Return exactly the contract JSON, without Markdown or explanation.",
      tools: { bash:false, read:false, edit:false, glob:false, grep:false, webfetch:false, websearch:false, task:false, todowrite:false, lsp:false, skill:false },
      parts: [{ type: "text", text: `${request}\n\nCOMPLETE NORMALIZED SOURCE TEXT:\n${source}` }],
    },
  });
  for (;;) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    const current = await client.session.messages({ path: { id: session.id }, query: { directory }, throwOnError: true });
    const latest = [...current.data].reverse().find((message) => message.info.role === "assistant");
    if (latest?.info?.error || latest?.parts?.some((part) => part.type === "text" && part.text.trim())) break;
  }
  const messages = await client.session.messages({ path: { id: session.id }, query: { directory }, throwOnError: true });
  const assistant = [...messages.data].reverse().find((message) => message.info.role === "assistant");
  if (!assistant || assistant.info.error) throw new Error(JSON.stringify(assistant?.info?.error ?? "no assistant response"));
  const output = assistant.parts.filter((part) => part.type === "text").map((part) => part.text).join("\n").trim();
  if (!output) throw new Error("empty OpenCode response");
  process.stdout.write(`${output}\n`);
} finally {
  clearTimeout(timer);
  server.close();
}
