import About from "@/components/About";
import AboutUs from "@/components/AboutUs";
import CodeTab from "@/components/CodeTab";
import HomePage from "@/components/HomePage";
import Innovate from "@/components/Innovate";
import JoinTheCommunity from "@/components/JoinTheCommunity";
import Navbar from "@/components/Navbar";
import { TracingBeamDemo } from "@/components/TracingBeamDemo";
import Image from "next/image";

export default function Home() {
  return (
    <div className="">
      <Navbar />
      <HomePage />
      <About />
      <CodeTab />
      <TracingBeamDemo />
      <JoinTheCommunity />
      {/* <AboutUs /> */}
    </div>
  );
}
