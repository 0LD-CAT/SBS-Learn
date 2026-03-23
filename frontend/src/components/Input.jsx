export default function Input({ placeholder, type = "text", ...props }) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className="w-full p-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
      {...props}
    />
  );
}