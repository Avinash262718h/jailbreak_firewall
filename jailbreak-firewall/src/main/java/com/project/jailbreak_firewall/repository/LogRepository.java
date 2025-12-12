package com.project.jailbreak_firewall.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.project.jailbreak_firewall.entity.SecurityLog;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface LogRepository extends JpaRepository<SecurityLog, Long> {
    List<SecurityLog> findAll();

    List<SecurityLog> findByJailbreakCategory(String jailbreakCategory);

    List<SecurityLog> findByHarmfulnessCategory(String harmfulnessCategory);
}