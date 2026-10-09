export type ArtifactType =
  | 'circuit'
  | 'compiled-circuit'
  | 'result'
  | 'histogram'
  | 'simulation-output'
  | 'attestation'
  | 'audit-export'
  | 'sbom'
  | 'evidence-package';

export interface Artifact {
  artifactId: string;
  jobId: string;
  artifactType: ArtifactType;
  storageUri: string;
  contentType?: string;
  sizeBytes?: number;
  hash: string;
  encrypted?: boolean;
  kmsKeyId?: string;
  retentionDays?: number;
  createdAt: string;
}
