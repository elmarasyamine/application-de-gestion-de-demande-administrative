import api from "./api";

export function sendMessage(message, userId) {
    return api.post("/chatbot/message", {
        message: message,
        userId: userId
    });
}
