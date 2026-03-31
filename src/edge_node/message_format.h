/*
 * SPECTRAL-EDGE: Distributed Message Passing Protocol
 * Phase 2 Design: Lightweight Anomaly Indicator Protocol
 * Target Hardware: ESP32-WROOM-32
 */

#ifndef SPECTRAL_EDGE_MESSAGE_H
#define SPECTRAL_EDGE_MESSAGE_H

#include <stdint.h>

// Defines the structure for neighbor-to-neighbor alert exchange
// Optimized for minimal communication overhead (bytes/round)
struct __attribute__((packed)) AnomalyAlertMessage {
    uint16_t node_id;           // Unique identifier of the transmitting IoT node
    uint32_t timestamp;         // Epoch time of the detected anomaly
    uint8_t  alert_level;       // 0: Normal, 1: Warning, 2: Critical (Attack)
    float    anomaly_score;     // Confidence score output from local ChebNet inference
    uint8_t  attack_class;      // Classified attack type (if alert_level > 0)
    uint16_t checksum;          // Simple validation to drop corrupted packets
};

// Expected payload size: 2 + 4 + 1 + 4 + 1 + 2 = 14 bytes per message
// This low byte-count satisfies the low-bandwidth constraint of IoT edge links.

#endif // SPECTRAL_EDGE_MESSAGE_H
