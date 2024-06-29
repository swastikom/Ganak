"use client";
 
import { motion } from "framer-motion";
import React from "react";
import { AuroraBackground } from "./ui/aurora-background";
import { Button } from "./ui/moving-border";
import Link from "next/link";


const HomePage = () => {
  

  return (
    <AuroraBackground>
    <motion.div
      initial={{ opacity: 0.0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{
        delay: 0.3,
        duration: 0.8,
        ease: "easeInOut",
      }}
      className="relative flex flex-col gap-4 items-center justify-center px-4"
    >
      <div className="text-3xl md:text-7xl font-bold dark:text-white text-center">
      AI for every developer
      </div>
      <div className="font-extralight text-base md:text-4xl dark:text-neutral-200 py-4">
      Build with state-of-the-art generative models and tools to make AI helpful for everyone
      </div>
      
      <Button
        borderRadius="1.75rem"
        className="bg-gradient-to-tr from-[#1d8efc] to-[#e85169] dark:bg-slate-900 text-black dark:text-white border-neutral-200 dark:border-slate-800 px-3 text-[15px]"
      >
       <Link href="/users">Chat with Ganak</Link> 
      </Button>
    </motion.div>
  </AuroraBackground>
  )
}

export default HomePage