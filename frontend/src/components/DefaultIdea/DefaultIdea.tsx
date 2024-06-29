import { IonIcon } from "@ionic/react";
import { sendOutline } from "ionicons/icons";
import useChat from "../../store/store";
import classNames from "classnames";
import { createMessage } from "@/utils/createMessage";


export default function DefaultIdea({
  ideas,
  myclassNames,
}: {
  ideas: { idea: string; moreContext: string }[];
  myclassNames?: string;
}) {
  const addChat = useChat((state: any) => state.addChat);
  return (
    <div
      className={classNames(
        "md:flex w-full md:gap-2 md:justify-between ",
        myclassNames
      )}
    >
      {ideas.map((i) => (
        <button
          key={i.idea}
          className=" inline-flex bg-gradient-to-b from-[#1e1f20] to-transparent  dark:hover:bg-gray-700 mb-2  w-[100px] h-[250px] text-left p-2 group rounded-[15px]  shadow flex-1 md:flex-row md:items-center"
          onClick={() => {
            addChat(createMessage("user", i.moreContext, "text"));
            addChat(createMessage("assistant", "", "text"));
          }}
        >
          <div className=" self-stretch w-11/12">
            <h3 className=" font-bold  dark:text-gray-300 text-gray-700">
              {i.idea}
            </h3>
            <p className=" dark:text-gray-400 text-gray-600">{i.moreContext}</p>
          </div>

          <div className="btn text-gray-600 dark:text-gray-200 text-lg invisible duration-75 transition-all group-hover:visible ">
            <IonIcon icon={sendOutline} />
          </div>
        </button>
      ))}
    </div>
  );
}
