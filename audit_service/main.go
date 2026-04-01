package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	opsProcessed = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "openlake_processed_ops_total",
		Help: "Número total de operações processadas pela plataforma.",
	})
	
	opsDuration = prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    "openlake_process_duration_seconds",
		Help:    "Tempo de duração do processamento.",
		Buckets: prometheus.DefBuckets,
	})
)

func init() {
	prometheus.MustRegister(opsProcessed, opsDuration)
}

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	slog.SetDefault(logger)

	mux := http.NewServeMux()

	mux.HandleFunc("/processar", func(w http.ResponseWriter, r *http.Request) {
		start := time.Now() // Inicia o cronômetro

		time.Sleep(50 * time.Millisecond)

		opsProcessed.Inc()
		opsDuration.Observe(time.Since(start).Seconds())

		slog.Info("Operação de auditoria realizada", "status", "sucesso", "ip", r.RemoteAddr)
		w.Write([]byte("Processado com sucesso!"))
	})

	mux.Handle("/metrics", promhttp.Handler())

	srv := &http.Server{
		Addr:         ":8080",
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	go func() {
		slog.Info("Servidor de Auditoria Iniciado", "porta", 8080)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			slog.Error("Erro fatal no servidor", "erro", err)
			os.Exit(1)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit

	slog.Info("Desligando o servidor graciosamente...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		slog.Error("Servidor forçado a fechar", "erro", err)
	}

	slog.Info("Servidor finalizado de forma segura.")
}
