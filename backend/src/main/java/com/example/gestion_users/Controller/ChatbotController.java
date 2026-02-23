package com.example.gestion_users.Controller;

import com.example.gestion_users.Dto.ChatbotRequest;
import com.example.gestion_users.Dto.ChatbotResponse;
import com.example.gestion_users.Service.facade.ChatbotService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/chatbot")
public class ChatbotController {

    @Autowired
    private ChatbotService chatbotService;

    @PostMapping("/message")
    public ChatbotResponse handleMessage(@RequestBody ChatbotRequest request) {
        return chatbotService.processMessage(request.getMessage(), request.getUserId());
    }
}
