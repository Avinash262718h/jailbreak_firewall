package com.project.jailbreak_firewall.service;

import com.project.jailbreak_firewall.entity.SecurityLog;
import com.project.jailbreak_firewall.repository.LogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;
import java.util.Map;

@Service
public class AnalysisService {

    @Autowired
    private LogRepository logRepository;

    private final RestTemplate restTemplate = new RestTemplate();

    private final String PYTHON_API_URL = "http://localhost:5000/analyze";

    @SuppressWarnings("unchecked")
    public SecurityLog analyzePrompt(String userPrompt) {

        Map<String, String> requestPayload = new HashMap<>();
        requestPayload.put("prompt", userPrompt);

        Map<String, Object> pythonResponse = null;
        try {
            pythonResponse = restTemplate.postForObject(PYTHON_API_URL, requestPayload, Map.class);
        } catch (Exception e) {
            System.out.println("⚠️ ERROR: Python Engine is down! " + e.getMessage());
        }

        SecurityLog log = new SecurityLog();
        log.setUserPrompt(userPrompt);

        if (pythonResponse != null) {
            log.setJailbreakScore(convertToDouble(pythonResponse.get("jailbreak_score")));
            log.setJailbreakCategory((String) pythonResponse.get("jailbreak_category"));

            log.setHarmfulnessScore(convertToDouble(pythonResponse.get("harmfulness_score")));
            log.setHarmfulnessCategory((String) pythonResponse.get("harmfulness_category"));

            log.setVerdict((String) pythonResponse.get("verdict"));
            log.setRecommendation((String) pythonResponse.get("recommendation"));
        } else {
            log.setVerdict("ERROR_ENGINE_OFFLINE");
            log.setRecommendation("Check if app.py is running on port 5000");
        }

        return logRepository.save(log);
    }

    private double convertToDouble(Object value) {
        if (value instanceof Number) {
            return ((Number) value).doubleValue();
        }
        return 0.0;
    }
}