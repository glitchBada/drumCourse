import Error404img from "../../imgs/404.png"
import "./Error404.scss";

function Error404 () {
return (
    <>
        <div className="error404">
            <div className="text404">
                <h1>404 - Страница не найдена</h1>
                <p>Извините, страница, которую вы ищете, не существует.</p>
                <a href="/home">Можете вернуться домой</a>
            </div>
            <img src={Error404img} alt="" />
        </div>
    </>
    );
}

export default Error404;