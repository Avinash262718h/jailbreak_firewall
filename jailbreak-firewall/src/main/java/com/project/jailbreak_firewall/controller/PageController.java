package com.project.jailbreak_firewall.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping("/")
    public String home() {
        return "index";
    }

    @GetMapping("/index.html")
    public String index() {
        return "index";
    }

    @GetMapping("/about.html")
    public String about() {
        return "about";
    }

    @GetMapping("/result.html")
    public String result() {
        return "result";
    }
}