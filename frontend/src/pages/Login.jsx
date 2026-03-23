import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { loginUser } from "../api/auth";
import PasswordInput from "../components/PasswordInput";
import githubIcon from "../assets/GitHub.png";
import vkIcon from "../assets/VK.png";
import googleIcon from "../assets/Google.png";

export default function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    login: "",
    password: "",
  });

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await loginUser(form);

      localStorage.setItem("token", res.result.access_token);

      navigate("/profile");
    } catch {
      alert("Ошибка входа");
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

        <form onSubmit={handleSubmit} className="space-y-5">

          {/* Email */}
          <div>
            <label className="text-sm text-gray-700">
              Почта / Логин
            </label>

            <input
              name="login"
              placeholder="Введите свой email или username"
              className="w-full mt-1 border border-borderInput rounded-xl p-3 outline-none focus:ring-2 focus:ring-primary"
              onChange={handleChange}
            />
          </div>

          {/* Password */}
          <div>
            <label className="text-sm text-gray-700">
              Пароль
            </label>

            <PasswordInput
              name="password"
              placeholder="********"
              onChange={handleChange}
            />

{/*             <div className="text-right mt-1"> */}
{/*               <span className="text-sm text-blue-500 cursor-pointer"> */}
{/*                 Забыли пароль? */}
{/*               </span> */}
{/*             </div> */}
          </div>

          {/* Button */}
          <button className="w-full bg-primary text-white rounded-xl py-3 font-medium hover:opacity-90">
            Войти
          </button>
        </form>

        {/* Divider */}
        <div className="flex items-center my-6">
          <div className="flex-grow border-t" />
          <span className="mx-3 text-sm text-textSecondary">
            Вход через соцсети
          </span>
          <div className="flex-grow border-t" />
        </div>

        {/* Social buttons */}
        <div className="space-y-3">

          <button className="w-full border rounded-full py-3 flex items-center justify-center gap-3 hover:bg-gray-50">

            <img
              src={vkIcon}
              className="w-5 h-5"
            />

            Продолжить с VK

          </button>


          <button className="w-full border rounded-full py-3 flex items-center justify-center gap-3 hover:bg-gray-50">

            <img
              src={googleIcon}
              className="w-5 h-5"
            />

            Продолжить с Google

          </button>


          <button className="w-full border rounded-full py-3 flex items-center justify-center gap-3 hover:bg-gray-50">

            <img
              src={githubIcon}
              className="w-5 h-5"
            />

            Продолжить с GitHub

          </button>

        </div>

        {/* Register link */}
        <div className="text-center mt-6">
          <Link
            to="/register"
            className="text-sm text-black-700 hover:text-primary"
          >
            Создать аккаунт
          </Link>
        </div>

      </div>
    </div>
  );
}