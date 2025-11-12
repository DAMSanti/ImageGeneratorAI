// Types para la generación de imágenes
export interface GenerateRequest {
  prompt: string;
  negative_prompt?: string;
  steps: number;
  guidance_scale: number;
  seed: number;
  width: number;
  height: number;
  sampler: string;
}

export interface GenerateResponse {
  success: boolean;
  image_url?: string;
  error?: string;
  parameters?: GenerateRequest;
}

export interface GeneratedImage {
  id: string;
  image_url: string;
  prompt: string;
  timestamp: string;
  parameters: GenerateRequest;
}

export interface Model {
  id: string;
  name: string;
  description: string;
}

export interface GenerationStatus {
  status: "idle" | "generating" | "completed" | "error";
  progress?: number;
  error?: string;
}
