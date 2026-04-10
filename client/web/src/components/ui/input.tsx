import * as React from "react";

import { cn } from "@/lib/cn";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        "flex h-10 w-full rounded-md border border-[var(--app-border)] bg-white px-3 py-2 text-sm text-[#22314d] outline-none placeholder:text-[#8d97a8] focus:ring-2 focus:ring-[#bfd0ff]",
        className,
      )}
      {...props}
    />
  );
});
Input.displayName = "Input";

export { Input };
