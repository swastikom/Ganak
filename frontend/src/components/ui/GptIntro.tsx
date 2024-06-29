// import {IonIcon} from "@ionic/react"
// import { sparkles } from "ionicons/icons";
import { useSettings } from "../../store/store";
import classNames from "classnames"

export default function GptIntro() {
  const [selectedModel, setModel] = useSettings((state: any) => [
    state.settings.selectedModal,
    state.setModal,
  ]);
  const isGptThreeSelected = selectedModel.startsWith("gpt-3");
  return (
    <>
      
      <div className=" h-96 flex items-start justify-center">
        <h1 className=" text-4xl font-bold mt-5 text-center text-gray-300">
          Ganak
        </h1>
      </div>
    </>
  );
}
