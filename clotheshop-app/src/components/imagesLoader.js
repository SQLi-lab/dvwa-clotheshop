// Динамически импортируем изображения
const importAll = (requireContext) => requireContext.keys().map(requireContext);
const images = importAll(require.context('../images', false, /\.(png|jpe?g|svg)$/));

export default images;
