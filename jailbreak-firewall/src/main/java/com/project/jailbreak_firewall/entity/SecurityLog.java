package com.project.jailbreak_firewall.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Column;
import lombok.Data;
import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;

@Entity
@Table(name = "security_log")
@Data
public class SecurityLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 5000)
    private String userPrompt;

    private double jailbreakScore;

    private String jailbreakCategory;

    private double harmfulnessScore;

    private String harmfulnessCategory;

    private String verdict;

    private String recommendation;

    @CreationTimestamp
    @Column(updatable=false)
    private LocalDateTime timestamp;

}