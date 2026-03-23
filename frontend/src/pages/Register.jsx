import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { registerUser } from "../api/auth";
import PasswordInput from "../components/PasswordInput";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    login: "",
    email: "",
    password: "",
  });

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await registerUser(form);

      navigate("/login");
    } catch {
      alert("Ошибка регистрации");
    }
  };

  return (
    <div className="min-h-screen bg-bgPage flex justify-center items-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-6 sm:p-8">

        {/* Logo */}
        <h1 className="text-2xl font-bold text-center mb-8">
          <span className="text-primary">Side</span>
          By
          <span className="text-red-500">Side</span>
          Learn
        </h1>

        {/* Title */}
        <h1 className="text-2xl font-bold mb-2">
          Регистрация
        </h1>

        <p className="text-sm text-textSecondary mb-6">
          Создайте новый аккаунт!
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">

          {/* Username */}
          <input
            name="login"
            placeholder="Введите своё имя/псевдоним"
            className="w-full border border-borderInput rounded-xl p-3"
            onChange={handleChange}
          />

          {/* Email */}
          <input
            name="email"
            placeholder="Введите свой email"
            className="w-full border border-borderInput rounded-xl p-3"
            onChange={handleChange}
          />

          {/* Password */}
          <PasswordInput
              name="password"
              placeholder="********"
              onChange={handleChange}
          />

          {/* Button */}
          <button className="w-full bg-primary text-white rounded-xl py-3 font-medium">
            Регистрация
          </button>

        </form>

        {/* Login link */}
        <div className="text-center mt-6 text-sm">
          Уже есть аккаунт?
          <Link
            to="/login"
            className="text-blue-500 ml-1"
          >
            Войти
          </Link>
        </div>

      </div>
    </div>
  );
}