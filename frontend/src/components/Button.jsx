export default function Button({ children, ...props }) {
  return (
    <button
      className="w-full bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-xl transition"
      {...props}
    >
      {children}
    </button>
  );
}