// SFTP gateway — SSH host keys, virtual paths, auth.
package main

import (
    "fmt"
    "log"
    "os"
)

func main() {
    hostKeyPath := os.Getenv("SFTP_HOST_KEY")
    if hostKeyPath == "" {
        log.Fatal("SFTP_HOST_KEY required")
    }
    fmt.Println("SFTP gateway starting (placeholder implementation)")
}
