"use client"

import Link from "next/link"
import { FC } from "react"
import { ChatbotUISVG } from "../icons/chatbotui-svg"

interface BrandProps {
  theme?: "dark" | "light"
}

export const Brand: FC<BrandProps> = ({ theme = "dark" }) => {
  return (
    <Link
      className="flex cursor-pointer flex-col items-center hover:opacity-50"
      href="https://www.chatbotui.com"
      target="_blank"
      rel="noopener noreferrer"
    >
      <div className="mb-2">
        <img src='/saarthi2.png' style={{
          height: '6rem',
          width: '6rem',
          borderRadius: '5rem'
        }} />
      </div>

      <div className="text-4xl font-bold tracking-wide">Saarthi</div>
    </Link>
  )
}
