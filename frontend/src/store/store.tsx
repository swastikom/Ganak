import { create } from "zustand";
import { persist } from "zustand/middleware";
import { createWithEqualityFn } from "zustand/traditional";
import { shallow } from "zustand/shallow";
import { produce } from "immer";
import moment from "moment";
import { ImageSize } from "../services/chatService";

const modalsList = [""] as const;

// Helper function to safely access localStorage
const getLocalStorage = () => {
  if (typeof window !== "undefined") {
    return window.localStorage;
  }
  return null;
};

export interface ChatMessageType {
  role: "user" | "assistant" | "system";
  content: string;
  type: "text" | "image_url";
  id: string;
}
export interface SystemMessageType {
  message: string;
  useForAllChats: boolean;
}
export interface ModalPermissionType {
  id: string;
  object: string;
  created: number;
  allow_create_engine: boolean;
  allow_sampling: boolean;
  allow_logprobs: boolean;
  allow_search_indices: boolean;
  allow_view: boolean;
  allow_fine_tuning: boolean;
  organization: string;
  group: null;
  is_blocking: boolean;
}
export interface ModalType {
  id: string;
  object: string;
  created: number;
  owned_by: string;
  permission: ModalPermissionType[];
  root: string;
  parent: null;
}
export type Theme = "light" | "dark";

export interface ThemeType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

export type ModalList = (typeof modalsList)[number];

export interface SettingsType {
  settings: {
    sendChatHistory: boolean;
    systemMessage: string;
    useSystemMessageForAllChats: boolean;
    selectedModal: ModalList;
    dalleImageSize: { "dall-e-2": ImageSize; "dall-e-3": ImageSize };
  };
  modalsList: readonly string[];
  isSystemMessageModalVisible: boolean;
  isModalVisible: boolean;
  setSystemMessage: (value: SystemMessageType) => void;
  setSystemMessageModalVisible: (value: boolean) => void;
  setSendChatHistory: (value: boolean) => void;
  setModalVisible: (value: boolean) => void;
  setModalsList: (value: string[]) => void;
  setModal: (value: ModalList) => void;
  setDalleImageSize: (value: ImageSize, type: "dall-e-2" | "dall-e-3") => void;
}
export interface ChatType {
  chats: ChatMessageType[];
  chatHistory: string[];
  addChat: (chat: ChatMessageType, index?: number) => void;
  editChatMessage: (chat: string, updateIndex: number) => void;
  addNewChat: () => void;
  saveChats: () => void;
  viewSelectedChat: (chatId: string) => void;
  resetChatAt: (index: number) => void;
  handleDeleteChats: (chatid: string) => void;
  editChatsTitle: (id: string, title: string) => void;
  clearAllChats: () => void;
}

export interface UserType {
  name: string;
  email: string;
  avatar: string;
}

export interface AuthType {
  token: string;
  apikey: string;
  setToken: (token: string) => void;
  setUser: (user: { name: string; email: string; avatar: string }) => void;
  setApiKey: (apikey: string) => void;
  user: UserType;
}

const useChat = create<ChatType>((set, get) => ({
  chats: [],
  chatHistory: (() => {
    const storage = getLocalStorage();
    if (storage) {
      const chatHistory = storage.getItem("chatHistory");
      return chatHistory ? JSON.parse(chatHistory) : [];
    }
    return [];
  })(),
  addChat: (chat, index) => {
    set(
      produce((state: ChatType) => {
        if (index || index === 0) state.chats[index] = chat;
        else {
          state.chats.push(chat);
        }
      })
    );
    if (chat.role === "assistant" && chat.content) {
      get().saveChats();
    }
  },
  editChatMessage: (chat, updateIndex) => {
    set(
      produce((state: ChatType) => {
        state.chats[updateIndex].content = chat;
      })
    );
  },
  addNewChat: () => {
    if (get().chats.length === 0) return;
    set(
      produce((state: ChatType) => {
        state.chats = [];
      })
    );
  },
  saveChats: () => {
    let chat_id = get().chats[0].id;
    let title;
    const storage = getLocalStorage();
    if (storage) {
      const storedChat = storage.getItem(chat_id);
      if (storedChat) {
        const data = JSON.parse(storedChat);
        if (data.isTitleEdited) {
          title = data.title;
        }
      }
    }
    const data = {
      id: chat_id,
      createdAt: new Date().toISOString(),
      chats: get().chats,
      title: title ? title : get().chats[0].content,
      isTitleEdited: Boolean(title),
    };

    if (storage) {
      storage.setItem(chat_id, JSON.stringify(data));
      if (!get().chatHistory.includes(chat_id)) {
        const updatedHistory = [...get().chatHistory, chat_id];
        storage.setItem("chatHistory", JSON.stringify(updatedHistory));
        set(
          produce((state: ChatType) => {
            state.chatHistory = updatedHistory;
          })
        );
      }
    }
  },
  viewSelectedChat: (chatId) => {
    const storage = getLocalStorage();
    if (storage) {
      const storedChat = storage.getItem(chatId);
      if (storedChat) {
        set(
          produce((state: ChatType) => {
            state.chats = JSON.parse(storedChat)?.chats ?? [];
          })
        );
      }
    }
  },
  resetChatAt: (index) => {
    set(
      produce((state: ChatType) => {
        state.chats[index].content = "";
      })
    );
  },
  handleDeleteChats: (chatid) => {
    set(
      produce((state: ChatType) => {
        state.chatHistory = state.chatHistory.filter((id) => id !== chatid);
        state.chats = [];
        const storage = getLocalStorage();
        if (storage) {
          storage.removeItem(chatid);
          storage.setItem("chatHistory", JSON.stringify(state.chatHistory));
        }
      })
    );
  },
  editChatsTitle: (id, title) => {
    const storage = getLocalStorage();
    if (storage) {
      const chatData = storage.getItem(id);
      if (chatData) {
        const chat = JSON.parse(chatData);
        chat.title = title;
        chat.isTitleEdited = true;
        storage.setItem(id, JSON.stringify(chat));
      }
    }
  },
  clearAllChats: () => {
    set(
      produce((state: ChatType) => {
        const storage = getLocalStorage();
        if (storage) {
          state.chatHistory.forEach((id) => {
            storage.removeItem(id);
          });
          storage.removeItem("chatHistory");
        }
        state.chats = [];
        state.chatHistory = [];
      })
    );
  },
}));

const useAuth = create<AuthType>()(
  persist(
    (set) => ({
      token: "",
      apikey: "",
      user: {
        name: "Your name?",
        email: "",
        avatar: "/imgs/default-avatar.jpg",
      },
      setToken: (token) => {
        set(
          produce((state) => {
            state.token = token;
          })
        );
      },
      setUser: (user) => {
        set(
          produce((state) => {
            state.user = user;
          })
        );
      },
      setApiKey: (apikey) => {
        set(
          produce((state) => {
            state.apikey = apikey;
          })
        );
        const storage = getLocalStorage();
        if (storage) {
          storage.setItem("apikey", apikey);
        }
      },
    }),
    {
      name: "auth",
    }
  )
);

const useSettings = createWithEqualityFn<SettingsType>()(
  persist(
    (set) => ({
      settings: {
        sendChatHistory: false,
        systemMessage: "",
        useSystemMessageForAllChats: false,
        selectedModal: "",
        dalleImageSize: { "dall-e-2": "256x256", "dall-e-3": "1024x1024" },
      },
      modalsList: modalsList,
      isSystemMessageModalVisible: false,
      isModalVisible: false,
      setSystemMessage: (value) => {
        set(
          produce((state: SettingsType) => {
            state.settings.systemMessage = value.message;
            state.settings.useSystemMessageForAllChats = value.useForAllChats;
          })
        );
      },
      setSystemMessageModalVisible: (value) => {
        set(
          produce((state: SettingsType) => {
            state.isSystemMessageModalVisible = value;
          })
        );
      },
      setSendChatHistory: (value) => {
        set(
          produce((state: SettingsType) => {
            state.settings.sendChatHistory = value;
          })
        );
      },
      setModal: (value) => {
        set(
          produce((state: SettingsType) => {
            state.settings.selectedModal = value;
          })
        );
      },
      setModalVisible: (value) => {
        set(
          produce((state: SettingsType) => {
            state.isModalVisible = value;
          })
        );
      },
      setModalsList: (value) => {
        set(
          produce((state: SettingsType) => {
            state.modalsList = value;
          })
        );
      },
      setDalleImageSize: (value, type) => {
        set(
          produce((state: SettingsType) => {
            state.settings.dalleImageSize[type] = value;
          })
        );
      },
    }),
    {
      name: "settings",
      version: 1,
      partialize: (state: SettingsType) => ({ settings: state.settings }),
      migrate: (persistedState: unknown, version: number) => {
        if (version === 0) {
          (persistedState as SettingsType["settings"]).dalleImageSize = {
            "dall-e-2": "256x256",
            "dall-e-3": "1024x1024",
          };
        }

        return persistedState as SettingsType;
      },
    }
  ),
  shallow
);

const useTheme = create<ThemeType>()(
  persist(
    (set) => ({
      theme: "dark",
      setTheme: (theme) => {
        set(
          produce((state) => {
            state.theme = theme;
          })
        );
      },
    }),
    {
      name: "theme",
    }
  )
);

export const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
export const priority = [
  "Today",
  "Previous 7 Days",
  "Previous 30 Days",
  "This month",
].concat(months);

export const selectChatsHistory = (state: ChatType) => {
  const sortedData: Record<
    string,
    { title: string; id: string; month: string; month_id: number }[]
  > = {};
  const storage = getLocalStorage();
  if (storage) {
    state.chatHistory.forEach((chat_id) => {
      const chatData = storage.getItem(chat_id);
      if (chatData) {
        const { title, id, createdAt } = JSON.parse(chatData);
        const myDate = moment(createdAt, "YYYY-MM-DD");
        const currentDate = moment();
        const month = myDate.toDate().getMonth();

        const data = {
          title,
          id,
          month: months[month],
          month_id: month,
        };

        if (myDate.isSame(currentDate.format("YYYY-MM-DD"))) {
          if (!sortedData.hasOwnProperty("Today")) {
            sortedData["Today"] = [];
          }
          sortedData["Today"].push(data);
        } else if (currentDate.subtract(7, "days").isBefore(myDate)) {
          if (!sortedData.hasOwnProperty("Previous 7 Days")) {
            sortedData["Previous 7 Days"] = [];
          }
          sortedData["Previous 7 Days"].push(data);
        } else if (currentDate.subtract(30, "days").isBefore(myDate)) {
          if (!sortedData.hasOwnProperty("Previous 30 Days")) {
            sortedData["Previous 30 Days"] = [];
          }
          sortedData["Previous 30 Days"].push(data);
        } else {
          if (!sortedData.hasOwnProperty(months[month])) {
            sortedData[months[month]] = [];
          }
          sortedData[months[month]].push(data);
        }
      }
    });
  }
  return sortedData;
};

export const selectUser = (state: AuthType) => state.user;
export const chatsLength = (state: ChatType) => state.chats.length > 0;
export const isDarkTheme = (state: ThemeType) => state.theme === "dark";
export const isChatSelected = (id: string) => (state: ChatType) =>
  state.chats[0]?.id === id;

export default useChat;
export { useAuth, useSettings, useTheme };
