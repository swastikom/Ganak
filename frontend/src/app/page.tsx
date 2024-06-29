import CodeTab from "@/components/CodeTab";
import HomePage from "@/components/HomePage";
import JoinTheCommunity from "@/components/JoinTheCommunity";
import Image from "next/image";

export default function Home() {
  return (
    <div className="">
      <HomePage />
      <CodeTab />
      <JoinTheCommunity />
    </div>
  );
}
