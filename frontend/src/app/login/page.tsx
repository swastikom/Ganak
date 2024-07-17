"use client";

import React, { useState, FormEvent } from "react";
import { login } from "@/services/auth";
import { useRouter } from "next/navigation";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await login({ username, password });
      console.log(response);
      localStorage.setItem("authToken", response.access_token);
      router.push("/chat");
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail);
      } else {
        setError("An unexpected error occurred.");
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p>{error}</p>}
        <button className="bg-yellow-400" type="submit">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
