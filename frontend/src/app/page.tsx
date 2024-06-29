import AboutUs from "@/components/AboutUs";
import CodeTab from "@/components/CodeTab";
import HomePage from "@/components/HomePage";
import Innovate from "@/components/Innovate";
import JoinTheCommunity from "@/components/JoinTheCommunity";
import { TracingBeamDemo } from "@/components/TracingBeamDemo";
import Image from "next/image";

export default function Home() {
  return (
    <div className="">
      <HomePage />
      <CodeTab />
      <TracingBeamDemo />
      <JoinTheCommunity />
      {/* <AboutUs /> */}
    </div>
  );
}
