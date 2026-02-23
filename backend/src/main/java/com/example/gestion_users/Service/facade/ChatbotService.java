package com.example.gestion_users.Service.facade;

import com.example.gestion_users.Dto.ChatbotResponse;

public interface ChatbotService {
    ChatbotResponse processMessage(String message, Long userId);
}
