import { useState } from "react";

export default function PasswordInput({
  placeholder,
  name,
  onChange,
}) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="relative">

      <input
        type={showPassword ? "text" : "password"}
        name={name}
        placeholder={placeholder}
        onChange={onChange}
        className="
          w-full
          border
          border-borderInput
          rounded-xl
          p-3
          pr-12
          outline-none
          focus:ring-2
          focus:ring-primary
        "
      />

      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
        className="
          absolute
          right-3
          top-1/2
          -translate-y-1/2
          text-gray-400
          hover:text-gray-600
        "
      >
        {showPassword ? "Скрыть" : "Показать"}
      </button>

    </div>
  );
}