package com.project.jailbreak_firewall.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import com.project.jailbreak_firewall.entity.SecurityLog;
import com.project.jailbreak_firewall.service.AnalysisService;

@RestController
@RequestMapping("/api/firewall")
@CrossOrigin(origins = "*")
public class JailbreakController {
    @Autowired
    private AnalysisService analysisService;

    @PostMapping("/check")
    public ResponseEntity<SecurityLog> analyzePrompt(@RequestBody Map<String, String> requestBody) {
        String userPrompt = requestBody.get("prompt");
        SecurityLog result = analysisService.analyzePrompt(userPrompt);
        return ResponseEntity.ok(result);
    }

}
