import { ChatMessageType, ModalList, useSettings } from "../store/store";

const apiUrl = "https://api.openai.com/v1/chat/completions";
const IMAGE_GENERATION_API_URL = "https://api.openai.com/v1/images/generations";

const BACKEND_URL = "https://ganak-xwdx.onrender.com";

export async function fetchResults(
  messages: Omit<ChatMessageType, "id" | "type">[],
  modal: string,
  signal: AbortSignal,
  onData: (data: string) => void,
  onCompletion: () => void
) {
  try {
    const authToken = localStorage.getItem("authToken");
    console.log("Auth Token (first few characters):", authToken?.substring(0, 10));
    if (!authToken) {
      throw new Error("Auth token not found");
    }

    const response = await fetch(`${BACKEND_URL}/users/me/save_contexts`, {
      method: 'POST',
      signal: signal,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        chat_input: messages[messages.length - 1].content,
      }),
    });

    console.log("Response status:", response.status);
    console.log("Response headers:", Object.fromEntries(response.headers));

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Error data:", errorData);
      throw new Error(errorData.detail || `Error fetching results: ${response.status}`);
    }

    const data = await response.json();
    console.log("Response data:", data);

    if (data.response) {
      onData(data.response);
    } else {
      console.warn("No response data received from the backend");
    }

    onCompletion();
  } catch (error) {
    console.error("Error in fetchResults:", error);
    throw error;
  }
}

export async function fetchModals() {
  try {
    const response = await fetch("https://api.openai.com/v1/models", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("apikey")}`,
      },
    });
    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof DOMException || error instanceof Error) {
      throw new Error(error.message);
    }
  }
}

export type ImageSize =
  | "256x256"
  | "512x512"
  | "1024x1024"
  | "1280x720"
  | "1920x1080"
  | "1792x1024"
  | "1024x1792";

export type IMAGE_RESPONSE = {
  created_at: string;
  data: IMAGE[];
};
export type IMAGE = {
  url: string;
};
export type DallEImageModel = Extract<ModalList, "dall-e-2" | "dall-e-3">;

export async function generateImage(
  prompt: string,
  size: ImageSize,
  numberOfImages: number
) {
  const selectedModal = useSettings.getState().settings.selectedModal;

  const response = await fetch(IMAGE_GENERATION_API_URL, {
    method: `POST`,
    headers: {
      "content-type": `application/json`,
      accept: `text/event-stream`,
      Authorization: `Bearer ${localStorage.getItem("apikey")}`,
    },
    body: JSON.stringify({
      model: selectedModal,
      prompt: prompt,
      n: numberOfImages,
      size: useSettings.getState().settings.dalleImageSize[
        selectedModal as DallEImageModel
      ],
    }),
  });
  const body: IMAGE_RESPONSE = await response.json();
  return body;
}
