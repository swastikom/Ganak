"use client";
 
import { motion } from "framer-motion";
import React from "react";
import { AuroraBackground } from "./ui/aurora-background";
import { Button } from "./ui/moving-border";
import Link from "next/link";
import { WavyBackground } from "./ui/wavy-background";
import { useRouter } from "next/navigation";


const HomePage = () => {
  const router = useRouter()
  const handleChange = () => {
    router.push('/chat')
  }

  return (
    <WavyBackground>
      <motion.div
      initial={{ opacity: 0.0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{
        delay: 0.3,
        duration: 0.8,
        ease: "easeInOut",
      }}
      className="relative flex flex-col gap-4 items-center justify-center px-4 text-white"
    >
      <div className="text-3xl md:text-7xl font-bold dark:text-white text-center">
      AI for every developer
      </div>
      <div className="font-extralight text-base md:text-4xl dark:text-neutral-200 py-4">
      Build with state-of-the-art generative models and tools to make AI helpful for everyone
      </div>
      
      <div onClick={handleChange}>
      <button
      
        className=" text-white border-neutral-200 dark:border-slate-800 px-3 p-3 bg-gradient-to-r from-[#0844ff] to-[#4793fc] hover:bg-gradient-to-r hover:from-white hover:to-white hover:text-[#4793fc] text-[15px] rounded-[30px]"
      >
       Chat with Ganak 
      </button>
      </div>
    </motion.div>
    </WavyBackground>
  )
}

export default HomePage