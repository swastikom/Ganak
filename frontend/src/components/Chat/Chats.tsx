import { Dialog, DialogTrigger } from "@radix-ui/react-dialog";
import useChat from "../../store/store";
import BotMessage from "./BotMessage";
import UserMessage from "./UserMessage";
import { Button } from "../ui/moving-border";
import { DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "../ui/dialog";

export default function Chats() {
  const chats = useChat((state) => state.chats);

  return (
    <div className="md:mt-10 w-full">
      <Dialog>
      <DialogTrigger asChild>
        <button className="px-3 py-2 bg-blue-600 rounded-[30px] ml-5">Check Your Score</button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <h1>Queries</h1>
          
        </div>
        <DialogFooter>
          <Button type="submit">Save changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
      {chats.map((chat, index) =>
        chat.role === "assistant" ? (
          <BotMessage index={index} key={chat.id} chat={chat} />
        ) : (
          <UserMessage chat={chat} chatIndex={index} key={chat.id} />
        )
      )}

      <div className="h-48 flex-shrink-0"></div>
    </div>
  );
}
